"""Module to handle the signal extraction of ROIs"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QProgressDialog
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
    approximate_frames = len(image_files) * 800

    # Set up outputs to store the fluorescence data
    fluorescence_data = {}
    for key, value in parent.ROIs.items():
        if value:
            fluorescence_data[key] = np.zeros(len(value)).reshape(1, -1)
            if key == "Dendrite":
                fluorescence_data["Dendrite Poly"] = [
                    np.zeros(len(roi.roi.poly_rois)).reshape(1, -1) for roi in value
                ]

    # Keep track of frames processed for progress bar
    frame_tracker = 0
    progress = QProgressDialog(
        "Extracting Fluorescence...", "Cancel", 0, approximate_frames,
    )
    progress.setMinimumDuration(0)
    progress.setWindowModality(Qt.WindowModal)
    progress.show()

    # Extract fluorescence for each image file
    for image_file in image_files:
        progress.setValue(frame_tracker)
        image = sio.imread(
            os.path.join(parent.image_directory, image_file), plugin="tifffile"
        )
        tif = image

        # Extract fluorescence for each ROI
        for key, value in parent.ROIs.items():
            if key == "Background":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                fluorescence_data["Background"] = np.append(
                    fluorescence_data["Background"], fluo, axis=0
                )
            elif key == "Soma":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                fluorescence_data["Soma"] = np.append(
                    fluorescence_data["Soma"], fluo, axis=0
                )
            elif key == "Spine":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                fluorescence_data["Spine"] = np.append(
                    fluorescence_data["Spine"], fluo, axis=0
                )
            elif key == "Dendrite":
                if not value:
                    continue
                fluo = get_roi_fluorescence(parent, key, value, tif)
                poly_mean = []
                for i, dend in enumerate(fluo):
                    poly_mean.append(dend.mean(axis=1).reshape(-1, 1))
                    fluorescence_data["Dendrite Poly"][i] = np.append(
                        fluorescence_data["Dendrite Poly"][i], dend, axis=0
                    )
                fluorescence_data["Dendrite"] = np.append(
                    fluorescence_data["Dendrite"], np.hstack(poly_mean), axis=0
                )

        frame_tracker = frame_tracker + np.shape(image)[0]
        progress.setValue(frame_tracker)

    # Remove the zeros generated during initialization
    for key, value in fluorescence_data.items():
        if key != "Dendrite Poly":
            fluorescence_data[key] = value[1:, :]
        else:
            new_value = []
            for v in value:
                new_value = v[1:, :]
            fluorescence_data["Dendrite Poly"] = new_value

    plt.figure()
    plt.plot(fluorescence_data["Dendrite"][:, 0])
    plt.savefig("test.pdf")


def get_roi_fluorescence(parent, roi_type, rois, arr):
    """Helper function to extract the fluorscence of ROIs from a single
        imaging frame"""
    if roi_type == "Soma" or roi_type == "Spine":
        roi_regions = []
        for roi in rois:
            array_region = roi.roi.getArrayRegion(
                arr=arr, img=parent.current_image, axes=(1, 2)
            )
            roi_regions.append(array_region.mean(axis=(1, 2)))
        roi_regions = np.vstack(roi_regions).T
        return roi_regions

    elif roi_type == "Background":
        array_region = rois[0].roi.getArrayRegion(
            arr=arr, img=parent.current_image, axes=(1, 2)
        )
        roi_regions = array_region.mean(axis=(1, 2))
        return roi_regions.reshape(-1, 1)

    elif roi_type == "Dendrite":
        roi_regions = []
        for roi in rois:
            poly_regions = []
            for poly_roi in roi.roi.poly_rois:
                poly_region = poly_roi.getArrayRegion(
                    arr=arr, img=parent.current_image, axes=(1, 2)
                )
                poly_regions.append(poly_region.mean(axis=(1, 2)).reshape(-1, 1))
            roi_regions.append(np.hstack(poly_regions))
        return roi_regions

