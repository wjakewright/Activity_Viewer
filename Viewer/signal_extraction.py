"""Module to handle the signal extraction of ROIs"""

import os

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog
from skimage import io as sio

import messages


def extract_raw_fluorescence(parent):
    """Function to extract the raw fluorescence for each ROI"""
    # Make some checks first
    try:
        float(parent.image_rate_input.text())
    except ValueError:
        messages.imaging_rate_warning(parent)
        return
    if not parent.ROIs["Background"]:
        messages.no_background_warning(parent)
        return
    if parent.ROIs["Spine"]:
        if not parent.ROIs["Dendrite"]:
            messages.parent_dendrite_warning(parent)
            return

    image_directory = QFileDialog.getExistingDirectory(
        parent, "Select Image Directory", options=QFileDialog.ShowDirsOnly
    )
    parent.image_directory = image_directory
    image_files = [
        img for img in os.listdir(parent.image_directory) if img.endswith(".tif")
    ]

    # Set up outputs to store the fluorescence data
    background_fluo = np.zeros(len(parent.ROIs["Background"])).reshape(1, -1)
    soma_fluo = np.zeros(len(parent.ROIs["Soma"])).reshape(1, -1)
    spine_fluo = np.zeros(len(parent.ROIs["Spine"])).reshape(1, -1)
    dendrite_fluo = np.zeros(len(parent.ROIs["Dendrite"])).reshape(1, -1)
    dendrite_poly_fluo = [
        np.zeros(len(roi.roi.poly_rois)).reshape(1, -1)
        for roi in parent.ROIs["Dendrite"]
    ]

    # Keep track of frames processed for progress bar
    frame_tracker = 0
    for image_file in image_files[:2]:
        image = sio.imread(
            os.path.join(parent.image_directory, image_file), plugin="tifffile"
        )

        tif = image

        for key, value in parent.ROIs.items():
            if key == "Background":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                background_fluo = np.append(background_fluo, fluo, axis=0)
            elif key == "Soma":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                soma_fluo = np.append(soma_fluo, fluo, axis=0)
            elif key == "Spine":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                spine_fluo = np.append(spine_fluo, fluo, axis=0)
            elif key == "Dendrite":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                poly_mean = []
                for i, dend in enumerate(fluo):
                    poly_mean.append(dend.mean(axis=1).reshape(-1, 1))
                    dendrite_poly_fluo[i] = np.append(
                        dendrite_poly_fluo[i], dend, axis=0
                    )
                dendrite_fluo = np.append(dendrite_fluo, np.hstack(poly_mean), axis=0)

    print(np.shape(background_fluo))
    print(soma_fluo)
    print(np.shape(spine_fluo))
    print(np.shape(dendrite_fluo))
    print(len(dendrite_poly_fluo))
    print(np.shape(dendrite_poly_fluo[0]))


def get_roi_fluorescence(parent, roi_type, rois, arr):
    """Helper function to extract the fluorscence of ROIs from a single
        imaging frame"""
    if roi_type == "Soma" or roi_type == "Spine":
        roi_regions = []
        for roi in rois:
            array_region = roi.roi.getArrayRegion(
                arr=arr, img=parent.current_image, axes=(2, 1)
            )
            roi_regions.append(array_region.mean(axis=(1, 2)))
        roi_regions = np.vstack(roi_regions).T
        return roi_regions

    elif roi_type == "Background":
        array_region = rois[0].roi.getArrayRegion(
            arr=arr, img=parent.current_image, axes=(2, 1)
        )
        roi_regions = array_region.mean(axis=(2, 1))
        return roi_regions.reshape(-1, 1)

    elif roi_type == "Dendrite":
        roi_regions = []
        for roi in rois:
            poly_regions = []
            for poly_roi in roi.roi.poly_rois:
                poly_region = poly_roi.getArrayRegion(
                    arr=arr, img=parent.current_image, axes=(2, 1)
                )
                print(np.shape(poly_region))
                poly_regions.append(poly_region.mean(axis=(1, 2)).reshape(-1, 1))
            print(np.shape(poly_regions[0]))
            roi_regions.append(np.hstack(poly_regions))
        return roi_regions

