"""Module to handle the signal extraction of ROIs"""

import os

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog

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

