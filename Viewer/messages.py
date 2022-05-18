"""Module for the creation of various message popups
    used by the GUI"""

from PyQt5.QtWidgets import QMessageBox, QPushButton

import display
import ROIs


def load_image_warning(parent):
    # Warning message to load image before drawing ROIs
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("No Image Loaded!!!")
    warning.setWindowTitle("Load Image Warning")
    # Button to load image from popup
    load_image_warning_btn = QPushButton("Load Image")
    load_image_warning_btn.clicked.connect(lambda: display.Load_File(parent))
    # Add Buttons to popup
    warning.addButton(load_image_warning_btn, QMessageBox.ActionRole)
    warning.setStandardButtons(QMessageBox.Cancel)
    retval = warning.exec()


def background_roi_warning(parent, view):
    # Warning that Background ROI has already been drawn
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("Background Already Drawn")
    warning.setWindowTitle("Background Warning")
    # Button to redraw the background roi
    redraw_background_btn = QPushButton("Redraw Background ROI")
    redraw_background_btn.clicked.connect(lambda: ROIs.redraw_background(parent, view))
    # Add Buttons to popup
    warning.addButton(redraw_background_btn, QMessageBox.ActionRole)
    warning.setStandardButtons(QMessageBox.Cancel)
    retval = warning.exec()


def delete_roi_warning(parent):
    # Warning messate to delete ROIs
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Question)
    warning.setText("Delete Selected ROIs? Deletion is final.")
    warning.setWindowTitle("Delete ROIs")
    # Button to delete the selected ROIs
    final_delete_roi_btn = QPushButton("Delete ROIs")
    final_delete_roi_btn.clicked.connect(lambda: ROIs.delete_ROIs(parent))
    # Add Buttons to popup
    warning.addButton(final_delete_roi_btn, QMessageBox.ActionRole)
    warning.setStandardButtons(QMessageBox.Cancel)
    retval = warning.exec()


def clear_roi_warning(parent):
    # Warning message to clear ROIs
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Question)
    warning.setText("Clear All ROIs? Clearing is final.")
    warning.setWindowTitle("Clear ROIs")
    # Button to clear the ROIs
    final_clear_roi_btn = QPushButton("Clear ROIs")
    final_clear_roi_btn.clicked.connect(lambda: ROIs.clear_ROIs(parent))
    # Add Buttons to popup
    warning.addButton(final_clear_roi_btn, QMessageBox.ActionRole)
    warning.setStandardButtons(QMessageBox.Cancel)
    retval = warning.exec()


def zoom_warning(parent):
    # Warning that zoom needs to be input
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("Must Input Image Zoom")
    warning.setWindowTitle("Image Zoom Input")
    # Button to clear warning
    warning.setStandardButtons(QMessageBox.Close)
    retval = warning.exec()


def parent_dendrite_warning(parent):
    # Warning that there is no dendrites for spines
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("No Dendrites Drawn")
    warning.setInformativeText(
        "Spines must have a parent dendrite \nPlease draw a dendrite"
    )
    warning.setWindowTitle("No Dendrites")
    # Button to clear warning
    warning.setStandardButtons(QMessageBox.Ok)
    retval = warning.exec()


def imaging_rate_warning(parent):
    # Warning that imaging rate has not been specified
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("Must Specify Imaging Acquisition Rate")
    warning.setWindowTitle("Imaging Rate")
    # Button to clear warning
    warning.setStandardButtons(QMessageBox.Ok)
    retval = warning.exec()


def no_background_warning(parent):
    # Warning that there is no background roi
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("No Background Drawn")
    warning.setInformativeText("Please draw background ROI")
    warning.setWindowTitle("No Background")
    # Button to clear warning
    warning.setStandardButtons(QMessageBox.Ok)
    retval = warning.exec()
