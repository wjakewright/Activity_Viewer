"""Module to preprocess fluorescence traces before calculating dFoF and 
    deconvolution"""

import numpy as np
from scipy import interpolate, stats


def preprocess_fluorescence(parent, parameters):
    """Function to preprocess traces"""
    fluorescence_subtracted = {}
    fluorescence_processed = {}
    drifting_basline = {}

    # Check bout separation correction
    if parameters["Correct Bout Separation"] is True:
        seps = parent.bout_separation_frames
    else:
        seps = None

    # Subtract background fluorescence
    for key, value in parent.ROI_fluorescence.items():
        if key != "Background":
            if key != "Dendrite Poly":
                fluorescence_subtracted[key] = (
                    value - parent.ROI_fluorescence["Background"]
                )
            else:
                dend_poly = []
                for v in value:
                    v_sub = v - parent.ROI_fluorescence["Background"]
                    dend_poly.append(v_sub)
                fluorescence_subtracted["Dendrite Poly"] = dend_poly
    ds_ratio = parameters["Ds Ratio"]
    # Correct the baseline using kernel density estimation
    for key, value in fluorescence_subtracted.items():
        print(key)
        if key != "Dendrite Poly":
            temp_f = np.zeros(np.shape(value))
            temp_b = np.zeros(np.shape(value))
            for i in range(np.shape(value)[1]):
                print(i)
                f, b = baseline_correction(
                    data=value[:, i],
                    ds_r=ds_ratio,
                    sampling_rate=parameters["Sampling Rate"],
                    bout_separations=seps,
                    artifact_frames=parameters["Artifact Frames"],
                )
                temp_f[:, i] = f
                temp_b[:, i] = b
            fluorescence_processed[key] = temp_f
            drifting_basline[key] = temp_b

        else:
            dend_poly_f = []
            dend_poly_b = []
            for j, v in enumerate(value):
                temp_f = np.zeros(np.shape(v))
                temp_b = np.zeros(np.shape(v))
                for i in range(np.shape(v)[1]):
                    f, b = baseline_correction(
                        data=v[:, i],
                        ds_r=ds_ratio,
                        sampling_rate=parameters["Sampling Rate"],
                        bout_separations=seps,
                        artifact_frames=parameters["Artifact Frames"],
                    )
                    temp_f[:, i] = f
                    temp_b[:, i] = b
                dend_poly_f.append(temp_f)
                dend_poly_b.append(temp_b)
            fluorescence_processed[key] = dend_poly_f
            drifting_basline[key] = dend_poly_b

    return fluorescence_subtracted, fluorescence_processed, drifting_basline


def baseline_correction(data, ds_r, sampling_rate, bout_separations, artifact_frames):
    """Function to correct time varying basline and also handle correction 
        of artifact frames and imaging bout separations
        
        INPUT PARAMETERS
            data - 1d array of fluorescence trace of a single roi
            
            sampling_rate - float indicating the imaging sampling rate
            
            bout_separations - list indicating which frames are the start of a new
                            imaging bout. e.g. when performing imaging loops
                            
            artifact_frames - list of tuples indicating the frames to black due to 
                            significant motion artifacts that are not corrected
                            (e.g., manual z correction)
        
        OUTPUT PARAMETERS
            corrected_fluorescence - array of corrected fluorescence trace

            drifting_basline - array of the estimated drifting baseline
    """

    # Constants
    DS_RATIO = ds_r
    WINDOW = np.round(sampling_rate)
    STEP = 20
    SECONDS_TO_IGNORE = 10  # for bout separations only
    PAD_LENGTH = 1000

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
    fluorescence_corrected = data - drifting_baseline

    return fluorescence_corrected, drifting_baseline


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

