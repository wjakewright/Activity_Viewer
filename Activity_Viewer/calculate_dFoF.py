"""Module for processing raw fluorescence traces to calculate deltaF/F. 
   Utilizes a drifting baseline across the entire session"""

import numpy as np
import scipy.signal as sysignal


def calulate_dFoF(data, baseline, sampling_rate, smooth_window=0.5):
    """Function to calculate dFoF from raw fluorescence traces
        
        INPUT PARAMETERS
            data - 1d array of preprocessed fluorescence trace of a single roi.

            baseline - 1d array of estimated baseline for a single roi

            smooth_window - float indicating over what time window to smooth the trace
                            Optional with default set to 0.5 seconds
            
            sample_rate - float indicating the imaging sampling rate. Default set to 30Hz

            
        OUTPUT PARAMETERS
            dFoF - array of the dFoF trace for the roi. 

            processed_dFoF - array of the smooth dFoF trace for the roi

    """
    # Constants
    SMOOTH_PAD_LENGTH = 500
    SMOOTH_WINDOW = int(smooth_window * np.round(sampling_rate))
    if SMOOTH_WINDOW % 2:
        SMOOTH_WINDOW = SMOOTH_WINDOW + 1

    # Baseline Division (since using raw fluorescence traces)
    if np.nanmedian(baseline) != 0:
        dFoF = data / baseline
    else:
        data = data + 1
        baseline = baseline + 1
        dFoF = data / baseline

    # Smooth the calculated dFoF
    pad_start = np.nanstd(dFoF) * np.random.randn(SMOOTH_PAD_LENGTH)
    pad_end = np.nanstd(dFoF) * np.random.randn(SMOOTH_PAD_LENGTH)

    padded_dFoF = np.concatenate((pad_start, dFoF, pad_end))
    padded_smoothed = sysignal.savgol_filter(padded_dFoF, SMOOTH_WINDOW, 2)
    #padded_smoothed = matlab_smooth(padded_dFoF, SMOOTH_WINDOW)

    processed_dFoF = padded_smoothed[SMOOTH_PAD_LENGTH:-SMOOTH_PAD_LENGTH]

    return dFoF, processed_dFoF


def matlab_smooth(data, window):
    """Helper function to replication the implementation of matlab smooth function
    
        data = 1d np.array
        
        window = int. Must be odd value
    """
    if window % 2 == 0:
        window = window + 1
    out0 = np.convolve(data, np.ones(window, dtype=int), "valid") / window
    r = np.arange(1, window - 1, 2)
    start = np.cumsum(data[: window - 1])[::2] / r
    stop = (np.cumsum(data[:-window:-1])[::2] / r)[::1]

    return np.concatenate((start, out0, stop))

