"""Module to handle the signal processing of the activity traces"""

import time

import numpy as np
from shapely.geometry import Point as ShP

from Activity_Viewer import (
    calculate_dFoF,
    deconvolve_calcium,
    messages,
    preprocess,
    spine_volume,
)
from Activity_Viewer.display import convert_pixels_to_um
from Activity_Viewer.event_detection import event_detection
from Activity_Viewer.output_window import Output_Window
from Activity_Viewer.processing_window import Processing_Window


def trigger_processing(parent):
    """Function to trigger processing the extracted signals
        
        Generates new window to allow inspection of the raw traces and 
        to specify information related to processing the activity traces
    """
    processing_window = Processing_Window(parent)
    processing_window.show()


def process_traces(parent, win):
    """Function to process the traces based on the parameters
        specified in the processing window"""
    # Check to make sure required inputs are there
    if hasattr(win, "grouping_frame"):
        for dend in win.grouping_input_list:
            if dend.text() == "":
                messages.dendrite_grouping_warning(parent)
                return

    # get processing parameters
    parameters = get_processing_params(parent, win)
    parent.parameters = parameters

    # get ROI spatial potisions
    print("Preprocessing")
    start_time = time.process_time()
    parent.ROI_positions = get_spatial_positions(parent, parameters)
    # subtract the time varying background from all the traces
    (
        parent.fluorescence_subtracted,
        parent.fluorescence_processed,
        parent.drifting_baseline,
    ) = preprocess.preprocess_fluorescence(parent, parameters)
    print("--- %4fs seconds ---" % (time.process_time() - start_time))

    # Calculate deltaF/F if specified
    if parameters["Calculate dFoF"] is True:
        print("Calculating dFoF")
        start_time = time.process_time()
        parent.dFoF, parent.processed_dFoF = get_dFoF(parent, parameters)

        (parent.activity_trace, parent.floored_trace, threshold_values,) = get_events(
            parent, parameters, parent.processed_dFoF
        )
        parent.parameters["Threshold Values"] = threshold_values
        print("--- %4fs seconds ---" % (time.process_time() - start_time))

    sensor = parameters["Imaging Sensor"]
    # Devonvolve traces if specified
    if parameters["Deconvolve"] is True and sensor != "iGluSnFr3":
        print("Deconvolving Traces")
        start_time = time.process_time()
        if sensor == "GCaMP6f":
            tau = 0.7
        elif sensor == "GCaMP6s":
            tau = 1.5
        elif sensor == "GCaMP7b":
            tau = 1.2
        elif sensor == "RCaMP2":
            tau = 1.0
        parent.deconvolved_spikes = get_deconvolved(parent, parameters, tau)
        print("--- %4fs seconds ---" % (time.process_time() - start_time))

    if parameters["Calculate Volume"] is True:
        print("Estimating Spine Volume")
        start_time = time.process_time()
        (
            parent.spine_pixel_intensity,
            parent.spine_volume,
            parent.dend_seg_intensity,
        ) = spine_volume.calculate_spine_volume(parent, parameters)

        (
            parent.corrected_spine_pixel_intensity,
            parent.corrected_spine_volume,
            parent.corrected_dend_seg_intensity,
        ) = spine_volume.calculate_spine_volume(parent, parameters, corrected=True)
        print("--- %4fs seconds ---" % (time.process_time() - start_time))

    win.close_window()
    output_window = Output_Window(parent)
    output_window.show()


def get_processing_params(parent, win):
    """Function to pull the parameters from the processing window"""

    # get all the parameter variables
    sensor = parent.imaging_sensor
    zoom = float(parent.zoom_input.text())
    sampling_rate = float(parent.image_rate_input.text())
    dFoF = win.dFoF_check_bx.isChecked()
    deconvolve = win.deconvolve_check_bx.isChecked()
    volume = win.volume_check_bx.isChecked()
    bout_sep = win.bout_sep_check_bx.isChecked()
    smooth = float(win.smooth_win_input.text())
    threshold = float(win.thresh_input.text())

    # Get artifact frames only if specified
    artifact_frames = []
    if win.artifact_input.text() != "":
        artifact_strs = win.artifact_input.text().split(";")
        for artifact in artifact_strs:
            start, stop = artifact.split("-")
            artifact_frames.append((int(start), int(stop)))

    # Get dend groupings is relevant
    dend_groupings = []
    if hasattr(win, "grouping_frame"):
        for dend in win.grouping_input_list:
            txt = dend.text().replace(" ", "")
            if "," in txt:
                txt = txt.split(",")
            if type(txt) == list:
                ss = []
                for t in txt:
                    try:
                        first, last = t.split("-")
                        s = list(range(int(first) - 1, int(last)))
                    except ValueError:
                        s = [int(t - 1)]
                    ss.append(s)
                spines = [x for xs in ss for x in xs]
            else:
                first, last = txt.split("-")
                spines = list(range(int(first) - 1, int(last)))
            dend_groupings.append(spines)

    # Package parameters into dictionary
    parameters = {
        "Imaging Sensor": sensor,
        "Zoom": zoom,
        "Sampling Rate": sampling_rate,
        "Calculate dFoF": dFoF,
        "Deconvolve": deconvolve,
        "Calculate Volume": volume,
        "Correct Bout Separation": bout_sep,
        "Smooth Window": smooth,
        "Threshold": threshold,
        "Artifact Frames": artifact_frames,
        "Spine Groupings": dend_groupings,
    }

    return parameters


def get_spatial_positions(parent, parameters):
    """Function to handel extracting the spatial positions for each roi
        Transforms pixel locations in to um values"""
    roi_positions = {}
    spine_groupings = parameters["Spine Groupings"]
    # Get um to pix conversion factors
    pix_conv = convert_pixels_to_um(parent)
    # Get positions for each roi
    for key, value in parent.ROIs.items():
        if key != "Background":
            # Get locations of somas relative to origin
            if key == "Soma":
                soma_coords = []
                for v in value:
                    roi = v.roi
                    roi_rect = roi.mapRectToParent(roi.boundingRect())
                    roi_coords_pix = roi_rect.center()
                    roi_coords_um = roi_coords_pix / pix_conv
                    roi_coords_um = (roi_coords_um.x(), roi_coords_um.y())
                    soma_coords.append(roi_coords_um)
                roi_positions["Soma"] = soma_coords

            # Get the positions of each dendrite poly roi
            elif key == "Dendrite":
                dend_coords = []
                for v in value:
                    coords = get_dend_coords(parent, v, pix_conv)
                    dend_coords.append(coords)
                roi_positions["Dendrite"] = dend_coords

            # Get the positions of spines along its parent dendrite
            elif key == "Spine":
                spine_coords = []
                for i, v in enumerate(value):
                    if spine_groupings:
                        for j, grouping in enumerate(spine_groupings):
                            if i in grouping:
                                group = j
                    else:
                        group = 0
                    roi = v.roi
                    coords = get_spine_coords(parent, roi, group, pix_conv)
                    spine_coords.append(coords)
                roi_positions["Spine"] = spine_coords

    return roi_positions


def get_dend_coords(parent, roi, pix_conv):
    """Function to get position of each dendrite poly roi along the 
        length of the dendrite"""
    dend_line = roi.roi.line
    roi_pos = []
    for poly in roi.roi.poly_rois:
        rect = poly.mapRectToParent(poly.boundingRect())
        x = rect.center().x()
        y = rect.center().y()
        point = ShP(x, y)
        dist = dend_line.project(point) / pix_conv
        roi_pos.append(dist)

    return roi_pos


def get_spine_coords(parent, roi, group, pix_conv):
    """Function to get spine positiotns along the length of its parent
        dendrite"""
    dend = parent.ROIs["Dendrite"][group]
    dend_line = dend.roi.line
    roi_rect = roi.mapRectToParent(roi.boundingRect())
    roi_coords = roi_rect.center()
    point = ShP(roi_coords.x(), roi_coords.y())
    dist = dend_line.project(point) / pix_conv

    return dist


def get_dFoF(parent, parameters):
    """Function to handle calculating dFoF for each ROI"""
    sampling_rate = parameters["Sampling Rate"]
    smooth_window = parameters["Smooth Window"]
    fluorescence = parent.fluorescence_processed
    baseline = parent.drifting_baseline

    dFoF = {}
    processed_dFoF = {}

    for (key, fluo), (_, base) in zip(fluorescence.items(), baseline.items()):
        if key != "Dendrite Poly":
            temp_df = np.zeros(np.shape(fluo))
            temp_pdf = np.zeros(np.shape(fluo))
            for i in range(np.shape(fluo)[1]):
                df, pdf = calculate_dFoF.calulate_dFoF(
                    data=fluo[:, i],
                    baseline=base[:, i],
                    sampling_rate=sampling_rate,
                    smooth_window=smooth_window,
                )
                temp_df[:, i] = df
                temp_pdf[:, i] = pdf
            dFoF[key] = temp_df
            processed_dFoF[key] = temp_pdf

        else:
            dend_poly_df = []
            dend_poly_pdf = []
            for f, b in zip(fluo, base):
                temp_df = np.zeros(np.shape(f))
                temp_pdf = np.zeros(np.shape(f))
                for i in range(np.shape(f)[1]):
                    df, pdf = calculate_dFoF.calulate_dFoF(
                        data=f[:, i],
                        baseline=b[:, i],
                        sampling_rate=sampling_rate,
                        smooth_window=smooth_window,
                    )
                    temp_df[:, i] = df
                    temp_pdf[:, i] = pdf
                dend_poly_df.append(temp_df)
                dend_poly_pdf.append(temp_pdf)
            dFoF[key] = dend_poly_df
            processed_dFoF[key] = dend_poly_pdf

    return dFoF, processed_dFoF


def get_events(parent, parameters, dFoF):
    """Helper function to handle event detection from dFoF"""
    threshold = parameters["Threshold"]
    sampling_rate = parameters["Sampling Rate"]

    activity_trace = {}
    floored_trace = {}
    threshold_values = {}

    for key, df in dFoF.items():
        if key != "Dendrite Poly":
            a_trace, f_trace, thresh = event_detection(df, threshold, sampling_rate)
            activity_trace[key] = a_trace
            floored_trace[key] = f_trace
            threshold_values[key] = thresh
        else:
            poly_a_trace = []
            poly_f_trace = []
            poly_thresh = []
            for poly_f in df:
                a_trace, f_trace, thresh = event_detection(
                    poly_f, threshold, sampling_rate
                )
                poly_a_trace.append(a_trace)
                poly_f_trace.append(f_trace)
                poly_thresh.append(thresh)

            activity_trace[key] = poly_a_trace
            floored_trace[key] = poly_f_trace
            threshold_values[key] = poly_thresh

    return activity_trace, floored_trace, threshold_values


def get_deconvolved(parent, parameters, tau):
    """Helper function to handel estimating deconvolved spikes
        from calcium fluorescence"""
    sampling_rate = parameters["Sampling Rate"]
    fluorescence = parent.fluorescence_processed
    batch_size = 500

    deconvolved_spikes = {}
    for key, fluo in fluorescence.items():
        if key != "Dendrite Poly":
            dspikes = deconvolve_calcium.oasis(
                fluo=fluo, batch_size=batch_size, tau=tau, sampling_rate=sampling_rate,
            )
            deconvolved_spikes[key] = dspikes
        else:
            dend_poly = []
            for poly in fluo:
                dspikes = deconvolve_calcium.oasis(
                    fluo=poly,
                    batch_size=batch_size,
                    tau=tau,
                    sampling_rate=sampling_rate,
                )
                dend_poly.append(dspikes)
            deconvolved_spikes[key] = dend_poly

    return deconvolved_spikes
