"""Module to handle the signal processing of the activity traces"""

import numpy as np

import calculate_dFoF
import messages
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
    background_subtraction(parent)

    # Calculate deltaF/F is specified
    if parameters["Calculate dFoF"] is True:
        get_dFoF(parent, parent.ROI_fluorescence_sub, parameters)


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


def background_subtraction(parent):
    """Function to subtract time varying background from fluorescence"""
    ROI_fluorescence_sub = {}
    print(np.shape(parent.ROI_fluorescence["Background"]))
    for key, value in parent.ROI_fluorescence.items():
        if key != "Background":
            ROI_fluorescence_sub[key] = value - parent.ROI_fluorescence["Background"]
    parent.ROI_fluorescence_sub = ROI_fluorescence_sub


def get_dFoF(parent, fluorescence, parameters):
    """Function to handle calculating the deltaF/F """
    # get bout separations if correcting
    if parameters["Correct Bout Separation"] is True:
        seps = parent.bout_separation_frames
    else:
        seps = None

    # calulate deltaF/F
    dFoF = {}
    processed_dFoF = {}
    drifting_baseline = {}
    for key, value in fluorescence.items():
        temp_dFoF = np.zeros(np.shape(value))
        temp_pdFoF = np.zeros(np.shape(value))
        temp_db = np.zeros(np.shape(value))
        for i in range(np.shape(value)[1]):
            df, pdf, db = calculate_dFoF.calulate_dFoF(
                data=value[:i],
                sampling_rate=parameters["Sampling Rate"],
                smooth_window=parameters["Smooth Window"],
                bout_separations=seps,
                artifact_frames=parameters["Artifact Frames"],
            )
            temp_dFoF[:, i] = df.reshape(-1, 1)
            temp_pdFoF[:, i] = pdf.reshape(-1, 1)
            temp_db[:, i] = db.reshape(-1, 1)

        dFoF[key] = temp_dFoF
        processed_dFoF[key] = temp_pdFoF
        drifting_baseline[key] = temp_db

    parent.dFoF = dFoF
    parent.processed_dFoF = processed_dFoF
    parent.drifting_baseline = drifting_baseline
