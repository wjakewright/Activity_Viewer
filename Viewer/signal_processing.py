"""Module to handle the signal processing of the activity traces"""

import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QCheckBox,
    QDesktopWidget,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
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
        parameters_window(self.parent, self)

        self.grid_layout.addWidget(self.param_widget, 0, 0)


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
