"""Module to handle the signal processing of the activity traces"""

import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QCheckBox,
    QDesktopWidget,
    QDialog,
    QGridLayout,
    QGroupBox,
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

    # Correct bout separations
    win.bout_sep_check_bx = QCheckBox("Correct Bout Separations", parent=win)
    win.bout_sep_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.bout_sep_check_bx.setFont(styles.roi_btn_font())

    # Add inputs to layout
    param_layout.addWidget(win.dFoF_check_bx)
    param_layout.addWidget(win.deconvolve_check_bx)
    param_layout.addWidget(win.bout_sep_check_bx)
    param_layout.addStretch(1)
