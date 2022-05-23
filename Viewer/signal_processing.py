"""Module to handle the signal processing of the activity traces"""

import matplotlib.pyplot as plt
import numpy as np

import calculate_dFoF
import deconvolve
import messages
import preprocess
from processing_window import Processing_Window


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

    # subtract the time varying background from all the traces
    (
        parent.fluorescence_subtracted,
        parent.fluorescence_processed,
        parent.drifting_baseline,
    ) = preprocess.preprocess_fluorescence(parent, parameters)

    # Calculate deltaF/F if specified
    if parameters["Calculate dFoF"] is True:
        parent.dFoF, parent.processed_dFoF = get_dFoF(parent, parameters)

    sensor = parameters["Imaging Sensor"]
    # Devonvolve traces if specified
    if parameters["Deconvolve"] is True and sensor != "iGluSnFr3":
        if sensor == "GCaMP6f":
            tau = 0.7
        elif sensor == "GCaMP6s":
            tau = 1.5
        elif sensor == "GCaMP7b":
            tau = 1.2
        elif sensor == "RCaMP2":
            tau = 1.0
        parent.deconvolved_spikes = get_deconvolved(parent, parameters, tau)

    plt.figure()
    plt.plot(parent.processed_dFoF["Soma"][:, 0])
    plt.savefig("test_dFoF.pdf")
    plt.figure()
    plt.plot(parent.deconvolved_spikes["Soma"][:, 0])
    plt.savefig("test_spikes.pdf")


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
            txt = dend.text()
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
        "Artifact Frames": artifact_frames,
        "Spine Groupings": dend_groupings,
    }

    return parameters


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


def get_deconvolved(parent, parameters, tau):
    """Helper function to handel estimating deconvolved spikes
        from calcium fluorescence"""
    sampling_rate = parameters["Sampling Rate"]
    fluorescence = parent.fluorescence_processed
    batch_size = 500

    deconvolved_spikes = {}
    for key, fluo in fluorescence.items():
        if key != "Dendrite Poly":
            dspikes = deconvolve.oasis(
                fluo=fluo, batch_size=batch_size, tau=tau, sampling_rate=sampling_rate,
            )
            deconvolved_spikes[key] = dspikes
        else:
            dend_poly = []
            for poly in fluo:
                dspikes = deconvolve.oasis(
                    fluo=poly,
                    batch_size=batch_size,
                    tau=tau,
                    sampling_rate=sampling_rate,
                )
                dend_poly.append(dspikes)
            deconvolved_spikes[key] = dend_poly

    return deconvolved_spikes
