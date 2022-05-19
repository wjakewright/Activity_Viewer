"""Module to handle the signal processing of the activity traces"""

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDesktopWidget,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

import styles


def start_processing(parent):
    """Function to start processing the extracted signals
        
        Generates new window to allow inspection of the raw traces and 
        to specify information related to processing the activity traces
    """
    processing_window = Processing_Window(parent)
    processing_window.show()


class Processing_Window(QDialog):
    """Custom Window to display extracted raw fluorescent traces and with inputs
        to specify how to further process the traces"""

    def __init__(self, parent):
        super(Processing_Window, self).__init__(parent=parent)

        self.parent = parent

        # Set up the window properties
        pg.setConfigOptions(imageAxisOrder="row-major")
        screen_size = QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.7)
        win_w = int(screen_size.width() * 0.7)
        self.setGeometry(70, 70, win_w, win_h)
        self.setWindowTitle("Process Fluorescence Traces")

        self.initWindow()

    def initWindow(self):
        """Putting everything into the window"""
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Make parameters window
        parameters_window(self.parent, self)

        # Make ROI list view
        roi_list_window(self.parent, self)

        self.side_box = QWidget()
        side_box_layout = QVBoxLayout()
        self.side_box.setLayout(side_box_layout)
        self.side_box.setFixedWidth(210)
        side_box_layout.addWidget(self.param_widget)
        side_box_layout.addWidget(self.roi_list_frame)
        side_box_layout.addStretch(1)

        self.grid_layout.addWidget(self.side_box, 0, 0)


def parameters_window(parent, win):
    # Layout for parameters in processing window
    param_layout = QVBoxLayout()
    win.param_widget = QGroupBox(win, title="Parameters")
    win.param_widget.setStyleSheet(styles.roiFrameStyle())
    win.param_widget.setFont(styles.roi_btn_font())
    win.param_widget.setLayout(param_layout)
    win.param_widget.setFixedWidth(200)

    # -----------ADD INPUTS-------------
    # Calculate dFoF
    win.dFoF_check_bx = QCheckBox("Calculate dFoF", parent=win)
    win.dFoF_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.dFoF_check_bx.setFont(styles.roi_btn_font())

    # Deconvolve
    win.deconvolve_check_bx = QCheckBox("Deconvolve Trace", parent=win)
    win.deconvolve_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.deconvolve_check_bx.setFont(styles.roi_btn_font())

    # Calculate Volume
    win.volume_check_bx = QCheckBox("Calculate Volume", parent=win)
    win.volume_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.volume_check_bx.setFont(styles.roi_btn_font())

    # Correct bout separations
    win.bout_sep_check_bx = QCheckBox("Correct Bout Separations", parent=win)
    win.bout_sep_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.bout_sep_check_bx.setFont(styles.roi_btn_font())

    # Smooth Window
    win.smooth_label = QLabel("Smooth Window")
    win.smooth_label.setStyleSheet(styles.parameterLabelStyle())
    win.smooth_label.setFont(styles.parameterLabelFont())
    win.smooth_win_input = QLineEdit()
    win.smooth_win_input.setStyleSheet(styles.parameterInputStyle())
    win.smooth_win_input.setFont(styles.roi_btn_font())
    if parent.imaging_sensor == "iGluSnFr3" or parent.imaging_sensor == "RCaMP2":
        default_smooth = "0.5"
    else:
        default_smooth = "0.0"
    win.smooth_win_input.setText(default_smooth)

    # Artifact Frames
    win.artifact_label = QLabel("Artifact Frames")
    win.artifact_label.setStyleSheet(styles.parameterLabelStyle())
    win.artifact_label.setFont(styles.parameterLabelFont())
    win.artifact_input = QLineEdit()
    win.artifact_input.setStyleSheet(styles.parameterInputStyle())
    win.artifact_input.setFont(styles.roi_btn_font())
    win.artifact_sublabel = QLabel("e.g., 10-40;80-100")
    win.artifact_sublabel.setStyleSheet(styles.parameterSubLabelStyle())
    win.artifact_sublabel.setFont(styles.parameterSubLabelFont())

    # Add inputs to layout
    param_layout.addWidget(win.dFoF_check_bx)
    param_layout.addWidget(win.deconvolve_check_bx)
    param_layout.addWidget(win.volume_check_bx)
    param_layout.addWidget(win.bout_sep_check_bx)
    param_layout.addWidget(win.smooth_label)
    param_layout.addWidget(win.smooth_win_input)
    param_layout.addWidget(win.artifact_label)
    param_layout.addWidget(win.artifact_input)
    param_layout.addWidget(win.artifact_sublabel)
    param_layout.addStretch(1)


def roi_list_window(parent, win):
    """Layout to display list of all rois that can be selected
        to display in the plot"""
    roi_list_layout = QVBoxLayout()
    win.roi_list_frame = QGroupBox(win, title="ROIs")
    win.roi_list_frame.setStyleSheet(styles.roiFrameStyle())
    win.roi_list_frame.setFont(styles.roi_btn_font())
    win.roi_list_frame.setLayout(roi_list_layout)
    win.roi_list_frame.setFixedWidth(200)

    win.ROI_list_window = QListWidget()
    win.ROI_list_window.setSelectionMode(QAbstractItemView.ExtendedSelection)
    win.ROI_list_window.setStyleSheet(styles.roiListStyle())

    # Get the ROI labels to display
    roi_labels = []
    for key, value in parent.ROIs.items():
        if not value:
            continue
        for i, _ in enumerate(value):
            label = f"{key} {i+1}"
            roi_labels.append(label)
            item = QListWidgetItem(label)
            win.ROI_list_window.addItem(item)

    roi_list_layout.addWidget(win.ROI_list_window)
    roi_list_layout.addStretch(1)
