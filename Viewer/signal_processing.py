"""Module to handle the signal processing of the activity traces"""

import numpy as np

from processing_window import Processing_Window


def start_processing(parent):
    """Function to start processing the extracted signals
        
        Generates new window to allow inspection of the raw traces and 
        to specify information related to processing the activity traces
    """
    processing_window = Processing_Window(parent)
    processing_window.show()

