"""Module to handle the signal processing of the activity traces"""

import numpy as np

from processing_window import Processing_Window


def trigger_processing(parent):
    """Function to trigger processing the extracted signals
        
        Generates new window to allow inspection of the raw traces and 
        to specify information related to processing the activity traces
    """
    processing_window = Processing_Window(parent)
    processing_window.show()


def process_traces(parent, win):
    """Function to process the traces based on the parameters
        specified in the processing window"""
    parameters = get_processing_params(win)


def get_processing_params(win):
    """Function to pull the parameters from the processing window"""
