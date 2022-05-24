"""Module to calculate the volume of individual spines"""

import os

import numpy as np

import images


def calculate_spine_volume(parent):
    """Function to estimate the volume of each spine ROI"""

    # Get average image projection to use for volume estimation
    avg_projection = get_total_avg_projection(parent)


def get_total_avg_projection(parent):
    """Helper function to get the average projection across all tif images"""
    # Get image file names
    image_files = [
        img for img in os.listdir(parent.image_directory) if img.endswith(".tif")
    ]

