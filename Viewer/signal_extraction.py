"""Module to handle the signal extraction of ROIs"""

import pyqtgraph as pg

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
