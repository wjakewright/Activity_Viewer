"""Module for processing raw fluorescence traces to calculate deltaF/F. 
   Utilizes a drifting baseline across the entire session"""

import numpy as np
from scipy import interpolate, stats


def calulate_dFoF(
    data, sampling_rate, smooth_window=0.5, bout_separations=None, artifact_frames=None
):
    """Function to calculate dFoF from raw fluorescence traces
        
        INPUT PARAMETERS
            data - 1d array of fluorescence trace of a single roi.

            smooth_window - float indicating over what time window to smooth the trace
                            Optional with default set to 0.5 seconds
            
            sample_rate - float indicating the imaging sampling rate. Default set to 30Hz

            bout_separations - list indicating which frames are the start of a new imaging bout.
                                e.g. when performing imaging loops
            
            artifact_frames - list of tuples indicating frames to blank due to significant 
                                motion artifacts that are not corrected (e.g. manual z correction)
        
        OUTPUT PARAMETERS
            dFoF - array of the dFoF trace for the roi. 

            processed_dFoF - array of the smooth dFoF trace for the roi

            drifting_baseline - array of the estimated drifting baseline used to 
                                calulate dFoF
    """
    # Constants
    DS_RATIO = 20
    WINDOW = np.round(sampling_rate)
    STEP = 20
    SECONDS_TO_IGNORE = 10  # only used to correct for bout separations
    PAD_LENGTH = 1000
    SMOOTH_PAD_LENGTH = 500
    SMOOTH_WINDOW = int(smooth_window * np.round(sampling_rate))

    if artifact_frames:
        jump_correction = True
    else:
        jump_correction = False

    # Fix NaN values for smoothing
    if np.isnan(data).any():
        # Get indecies of NaN values
        nan_inds = np.nonzero(np.isnan(data))[0]
        # Check if there is something wrong with the start of the trace
        first_val = np.nonzero(~np.isnan(data))[0][0]
        # Replace missing frames with baseline estimation
        if first_val > 10:
            data[:first_val] = baseline_kde(
                data[first_val : first_val + first_val - 1],
                ds_ratio=DS_RATIO,
                window=WINDOW,
                step=STEP,
            )
        # Get rid of NaN values. Mimic noisy trace
        data[nan_inds] = np.nanmedian(data) * np.ones(
            np.sum(np.isnan(data))
        ) + np.nanstd(data) * np.random.randn(np.sum(np.isnan(data)))

    # Fix data near zero
    if np.any(data < 1):
        data = data + np.absolute(np.nanmin(data))

    ## Pad data to prevent edge effects when estimating the baseline

    # Bounded curve that roughly estimates the baseline which will be used to padd data
    est_base = baseline_kde(data, DS_RATIO, WINDOW, STEP)

    # Remove start frames between imaging bouts (removes z shifts and photoactivation artifacts)
    if bout_separations is not None:
        start_frames = np.array([0] + bout_separations)
        blank_windows = start_frames + np.ceil(SECONDS_TO_IGNORE * sampling_rate)

        for start, ignore in zip(start_frames, blank_windows):
            if start > len(data):
                continue
            if ignore > len(data):
                ignore = len(data)
            data[start:ignore] = est_base[start:ignore] + np.nanstd(
                data
            ) * np.random.randn(len(np.arange(start, ignore)))

    # Correct for large uncorrected motion artifacts
    if jump_correction is True:
        for artifact in artifact_frames:
            start = artifact[0]
            end = artifact[1]
            data[start:end] = est_base[start:end] + (
                0.5 * np.nanstd(data[start:end])
            ) * np.random.randn(len(np.arange(start, end)))

    # Generate baseline
    pad_start = est_base[np.random.randint(low=0, high=1000, size=PAD_LENGTH)]
    pad_end = est_base[
        np.random.randint(
            low=len(est_base) - PAD_LENGTH, high=len(est_base), size=PAD_LENGTH
        )
    ]
    padded_data = np.concatenate((pad_start, data, pad_end))

    # Kernel Density Estimation (Aki's method)
    true_baseline_kde = baseline_kde(padded_data, DS_RATIO, WINDOW, STEP)
    drifting_baseline = true_baseline_kde[PAD_LENGTH:-PAD_LENGTH]

    # Baseline subtraction
    bl_sub = data - drifting_baseline

    # Baseline Division (since using raw fluorescence traces)
    if np.nanmedian(drifting_baseline) != 0:
        dFoF = bl_sub / drifting_baseline
    else:
        bl_sub = bl_sub + 1
        drifting_baseline = drifting_baseline + 1
        dFoF = bl_sub / drifting_baseline

    # Smooth the calculated dFoF
    pad_start = np.nanstd(dFoF) * np.random.randn(SMOOTH_PAD_LENGTH)
    pad_end = np.nanstd(dFoF) * np.random.randn(SMOOTH_PAD_LENGTH)

    padded_dFoF = np.concatenate((pad_start, dFoF, pad_end))
    padded_smoothed = matlab_smooth(padded_dFoF, SMOOTH_WINDOW)

    processed_dFoF = padded_smoothed[SMOOTH_PAD_LENGTH:-SMOOTH_PAD_LENGTH]

    return dFoF, processed_dFoF, drifting_baseline


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


def baseline_kde(x, ds_ratio, window, step):
    """Estimates fluorescence baseline using kernel density estimation
    
    INPUT PARAMETERS
        x - array of fluorescence traces
        
        ds_ratio - int specifying the downsample ratio
        
        window - int specifying the number of donwsampled samples to use baseline est
        
        step - int specifying the stepsize to increase speed
        
    OUTPUT PARAMETERS
        estimated_baseline - array of the estimated baseline
        
    """
    # Ensure parity between window and step sizes
    if window % 2 != step % 2:
        window = window + 1

    # downsample data
    x_ds = downsample_mean(x, ds_ratio)
    # Get where the downsampled points lie along the original array
    i_ds = downsample_mean(np.arange(len(x)), ds_ratio)

    h = (window - step) / 2

    i_steps = []
    b_steps = []
    for i in np.arange(0, len(x_ds), step):
        r = int(np.amax(np.array([0, i - h])))
        l = int(np.amin(np.array([len(x_ds), i + step - 1 + h])))
        i_steps.append(
            np.nanmean(i_ds[i : np.amin(np.array([i + step - 1, len(x_ds)]))])
        )
        b_steps.append(mode_kde(x_ds[r:l]))

    baseline_interpolater = interpolate.interp1d(
        i_steps, b_steps, kind="cubic", fill_value="extrapolate"
    )
    estimated_baseline = baseline_interpolater(np.arange(len(x)))

    return estimated_baseline


def mode_kde(x):
    # Helper function to perform the baseline kernel density estimation
    x = x[~np.isnan(x)]
    kde = stats.gaussian_kde(x)
    pts = np.linspace(x.min(), x.max(), 200)
    f = kde(pts)
    ii = np.nanargmax(f)
    ii_1 = np.amax(np.array([ii - 1, 1]))
    ii_2 = np.amin(np.array([ii + 1, len(f)]))

    if ii_2 - ii_1 == 2:
        if f[ii_2] > f[ii_1]:
            if f[ii] - f[ii_2] < f[ii_2] - f[ii_1]:
                ii_1 = ii
        else:
            if f[ii] - f[ii_1] < f[ii_1] - f[ii_2]:
                ii_2 = ii

    xx = np.linspace(pts[ii_1], pts[ii_2], 201)
    new_f = kde(xx)
    new_ii = np.nanargmax(new_f)

    m = xx[new_ii]

    return m


def downsample_mean(x, ds_ratio):
    # Helper function to downsample the data
    end = ds_ratio * int(len(x) / ds_ratio)
    ds = np.nanmean(x[:end].reshape(-1, ds_ratio), 1)

    return ds

