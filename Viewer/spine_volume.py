"""Module to calculate the volume of individual spines"""

import os

import numpy as np
from skimage import io as sio


def calculate_spine_volume(parent):
    """Function to estimate the volume of each spine ROI"""
    # Dendrite length constant to normalize to
    DEND_LEN = 20

    # Get average image projection to use for volume estimation
    avg_projection = get_total_avg_projection(parent)

    # Get ROI pixels from the avg projection image
    roi_pixels = {}
    for key, value in parent.ROIs.items():
        if key != "Soma":
            if key == "Background" or key == "Spine":
                pixels = []
                for v in value:
                    p = v.roi.getArrayRegion(
                        arr=avg_projection, img=parent.current_image, axes=(0, 1)
                    )
                    pixels.append(p)
                roi_pixels[key] = pixels
            elif key == "Dendrite":
                dend_pixels = []
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
    for spine in roi_pixels["Spine"]:
        above_background = spine[spine - background > 0] - background
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
    nomralized_spine_intensity = []


def get_total_avg_projection(parent):
    """Helper function to get the average projection across all tif images"""
    # Get image file names
    image_files = [
        img for img in os.listdir(parent.image_directory) if img.endswith(".tif")
    ]
    frame_tracker = 0
    summed_files = []
    for image in image_files:
        image = sio.imread(
            os.path.join(parent.image_directory, image), plugin="tifffile"
        )
        summed_image = np.sum(image, axis=0)
        frame_tracker = frame_tracker + np.shape(image)[0]
        summed_files.append(summed_image)

    average_projection = np.sum(summed_files, axis=0) / frame_tracker

    return average_projection
