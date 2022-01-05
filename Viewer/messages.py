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


def background_roi_warning(parent,view):
    # Warning that Background ROI has already been drawn
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("Background Already Drawn")
    warning.setWindowTitle("Background Warning")
    # Button to redraw the background roi
    redraw_background_btn = QPushButton("Redraw Background ROI")
    redraw_background_btn.clicked.connect(
        lambda: ROIs.redraw_background(parent, view)
    )
    # Add Buttons to popup
    warning.addButton(redraw_background_btn, QMessageBox.ActionRole)
    warning.setStandardButtons(QMessageBox.Cancel)
    retval = warning.exec()

