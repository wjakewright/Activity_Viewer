"""Module to handle the signal extraction of ROIs"""

import os

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QProgressDialog
from skimage import io as sio

from Activity_Viewer import messages, signal_processing


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
    print(parent.image_directory)
    image_directory = QFileDialog.getExistingDirectory(
        parent,
        "Select Image Directory",
        directory=parent.image_directory,
        options=QFileDialog.ShowDirsOnly,
    )
    parent.image_directory = image_directory
    image_files = [
        img for img in os.listdir(parent.image_directory) if img.endswith(".tif")
    ]
    print(image_files)
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

    # Keep track of how many frames are in each tif images
    frame_counts = []

    # Extract fluorescence for each image file
    for image_file in image_files:
        progress.setValue(frame_tracker)
        image = sio.imread(
            os.path.join(parent.image_directory, image_file), plugin="tifffile"
        )
        tif = image
        frame_counts.append(np.shape(tif)[0])
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
                new_v = v[1:, :]
                new_value.append(new_v)
            fluorescence_data["Dendrite Poly"] = new_value

    parent.ROI_fluorescence = fluorescence_data
    parent.bout_separations = find_bout_separations(image_files, frame_counts)
    signal_processing.trigger_processing(parent)


def get_roi_fluorescence(parent, roi_type, rois, arr):
    """Helper function to extract the fluorscence of ROIs from a single
        imaging frame"""
    if roi_type == "Spine":
        roi_regions = []
        for roi in rois:
            array_region = roi.roi.getArrayRegion(
                arr=arr, img=parent.current_image, axes=(1, 2)
            )
            roi_regions.append(array_region.sum(axis=(1, 2)))
        roi_regions = np.vstack(roi_regions).T
        return roi_regions

    if roi_type == "Soma":
        roi_regions = []
        for roi in rois:
            array_region, array_coords = roi.roi.getArrayRegion(
                arr=arr, img=parent.current_image, axes=(1, 2), returnMappedCoords=True,
            )
            # Create ROI to get the neuropil
            neuropil = pg.EllipseROI(
                pos=(roi.roi.pos()[0], roi.roi.pos()[1]),
                size=(roi.roi.size()[0] + 2, roi.roi.size()[1] + 2),
                parent=parent.current_image,
                removable=True,
            )
            neuropil_region, neuropil_coords = neuropil.getArrayRegion(
                arr=arr, img=parent.current_image, axes=(1, 2), returnMappedCoords=True,
            )
            # Remove neuropil roi
            parent.display_image.removeItem(neuropil)
            del neuropil
            print(f"full coords: {array_coords}")
            print(f"coords: {array_coords.shape}")
            print(f"full n coords: {neuropil_coords}")
            print(f"n coords: {neuropil_coords.shape}")
            roi_regions.append(array_region.sum(axis=(1, 2)))
            print(f"roi region: {array_region.sum(axis=(1,2)).shape}")
        roi_regions = np.vstack(roi_regions).T
        print(f"stack region: {roi_regions.shape}")

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
                poly_regions.append(poly_region.sum(axis=(1, 2)).reshape(-1, 1))
            roi_regions.append(np.hstack(poly_regions))
        return roi_regions


def find_bout_separations(images, frame_counts):
    """Function to find the frames seperating seperate imaging bouts within
        the same imaging session
        
        Returns a list of containing the index of the first frame at the 
        start of a new bout"""

    previous_frames = 0
    bout_ids = []
    bout_separations = []
    for i, (image, count) in enumerate(zip(images, frame_counts)):
        bout = image.split("_")[-3]
        bout_ids.append(bout)
        start_frame = previous_frames
        if i > 0:
            if bout != bout_ids[i - 1]:
                bout_separations.append(start_frame)
        else:
            bout_separations.append(start_frame)
        previous_frames = previous_frames + count

    return bout_separations

