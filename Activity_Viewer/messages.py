"""Module for the creation of various message popups
    used by the GUI"""

from PyQt5.QtWidgets import QMessageBox, QPushButton

from Activity_Viewer import ROIs, display, output


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


def dendrite_grouping_warning(parent):
    # Warning that you must specify dendrite groupings if more than one dendrite
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Warning)
    warning.setText("No Spine Groupings")
    warning.setInformativeText(
        "Must specify which spines belong to which dendrite before peceeding"
    )
    warning.setWindowTitle("Spine Groupings")
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


def save_ROI_warning(parent):
    # Warning to save rois before closing main window
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Question)
    warning.setText("Save ROIs before exiting?")
    warning.setWindowTitle("Save ROIs")
    # Save ROI button
    save_btn = QPushButton("Save")
    save_btn.clicked.connect(lambda: ROIs.save_ROIs(parent))
    warning.addButton(save_btn, QMessageBox.ActionRole)
    warning.setStandardButtons(QMessageBox.Close)
    retval = warning.exec()


def save_output_warning(parent):
    # Warning to save output before closing output window
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Question)
    warning.setText("Save output before exiting?")
    warning.setWindowTitle("Save Output")
    # Save output button
    save_btn = QPushButton("Save")
    save_btn.clicked.connect(lambda: output.output_data(parent))
    warning.addButton(save_btn, QMessageBox.ActionRole)
    warning.setStandardButtons(QMessageBox.Close)
    retval = warning.exec()


def load_ROI_flags_message(parent):
    # Message to ask if you wish to load all ROI flags intact
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Question)
    warning.setText("Load New Spine ROI Flags?")
    warning.setInformativeText("If not, still loads other flags")
    warning.setWindowTitle("Load ROI Flags")
    # Yes button
    yes_btn = QPushButton("Yes")
    yes_btn.clicked.connect(lambda: ROIs.set_flag_loading(parent, True))
    warning.addButton(yes_btn, QMessageBox.ActionRole)
    # No button
    no_btn = QPushButton("No")
    no_btn.clicked.connect(lambda: ROIs.set_flag_loading(parent, False))
    warning.addButton(no_btn, QMessageBox.ActionRole)
    retval = warning.exec()
