"""Module to calculate the volume of individual spines"""

import os

import numpy as np
from skimage import io as sio


def calculate_spine_volume(parent, parameters, corrected=False):
    """Function to estimate the volume of each spine ROI"""
    # Dendrite length constant to normalize to
    DEND_LEN = 20

    # Get average image projection to use for volume estimation
    # avg_projection = get_total_avg_projection(parent, exclude_frames)

    # Get ROI pixels from the avg projection image
    roi_pixels = {}
    for key, value in parent.ROIs.items():
        if key != "Soma":
            if key == "Background" or key == "Spine":
                pixels = []
                for i, v in enumerate(value):
                    if corrected:
                        activity = parent.activity_trace[key][:, i]
                        inactive = np.nonzero(activity == 0)[0]
                        avg_projection = get_total_avg_projection(
                            parent, include_frames=inactive
                        )
                    else:
                        avg_projection = get_total_avg_projection(
                            parent, include_frames=None
                        )
                    p = v.roi.getArrayRegion(
                        arr=avg_projection, img=parent.current_image, axes=(0, 1)
                    )
                    pixels.append(p)
                roi_pixels[key] = pixels
            elif key == "Dendrite":
                dend_pixels = []
                avg_projection = get_total_avg_projection(parent, indluce_frames=None)
                for v in value:
                    poly_pixels = []
                    for poly in v.roi.poly_rois:
                        p = poly.getArrayRegion(
                            arr=avg_projection, img=parent.current_image, axes=(0, 1)
                        )
                        poly_pixels.append(p)
                    dend_pixels.append(poly_pixels)
                roi_pixels[key] = dend_pixels

    background = np.nanmean(roi_pixels["Background"])

    # Get the integrated intensity of each spine roi
    integrated_spine_intensity = []
    spine_pix_intensity = []
    for spine in roi_pixels["Spine"]:
        above_background = spine[spine - background > 0] - background
        spine_pix_intensity.append(above_background)
        integrated_spine_intensity.append(np.nansum(above_background))

    # Get mean intensity for each poly roi for each dendrite
    mean_dend_intensity = []
    for dend in roi_pixels["Dendrite"]:
        poly_intensity = []
        for poly in dend:
            background_sub = poly - background
            poly_intensity.append(np.mean(background_sub))
        mean_dend_intensity.append(poly_intensity)

    # Normalize spine intensity to 20um of local dendrite
    normalized_spine_intensity = []
    dend_segment_intensity = []
    for i, spine in enumerate(integrated_spine_intensity):
        # First match spine to its parent dendrite
        if parameters["Spine Groupings"]:
            for j, grouping in enumerate(parameters["Spine Groupings"]):
                if i in grouping:
                    group = j
        else:
            group = 0
        parent_dend = mean_dend_intensity[group]
        parent_dend_pos = parent.ROI_positions["Dendrite"][group]
        parent_dend_pos_to_spine = (
            np.array(parent_dend_pos) - parent.ROI_positions["Spine"][i]
        )
        local_dend_idx = np.where(
            (parent_dend_pos_to_spine > -10) & (parent_dend_pos_to_spine < 10)
        )[0]

        local_dend = np.nanmean(np.array(parent_dend)[local_dend_idx])
        norm_spine = spine / local_dend
        normalized_spine_intensity.append(norm_spine)
        dend_segment_intensity.append(local_dend)

    return spine_pix_intensity, normalized_spine_intensity, dend_segment_intensity


def get_total_avg_projection(parent, include_frames=None):
    """Helper function to get the average projection across all tif images"""
    # Get image file names
    image_files = [
        img for img in os.listdir(parent.image_directory) if img.endswith(".tif")
    ]
    frame_tracker = 0
    image_frames = 0
    summed_files = []
    for image in image_files:
        image = sio.imread(
            os.path.join(parent.image_directory, image), plugin="tifffile"
        )
        frame_tracker = frame_tracker + np.shape(image)[0]
        if include_frames:
            include_frames = include_frames - frame_tracker
            include = [x for x in include_frames if x > 0 and x <= np.shape(image)[0]]
            image = image[include_frames, :, :]
        summed_image = np.sum(image, axis=0)
        image_frames = image_frames + np.shape(image)[0]
        summed_files.append(summed_image)

    average_projection = np.sum(summed_files, axis=0) / image_frames

    return average_projection
