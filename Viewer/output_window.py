"""Module for creating window to visualize the final outputs after processing"""

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import styles


class Output_Window(QDialog):
    """Custom window to display the outputs after processing"""

    def __init__(self, parent):
        super(Output_Window, self).__init__(parent=parent)
        self.parent = parent

        # Set up window properties
        pg.setConfigOptions(imageAxisOrder="row-major")
        screen_size = QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.7)
        win_w = int(screen_size.width() * 0.7)
        self.setGeometry(70, 70, win_w, win_h)
        self.setWindowTitle("Examine Outputs")

        self.initWindow()

    def initWindow(self):
        """Putting everything in the window"""

        self.current_data = []

        # Set up grid layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Make data display control frame
        display_control_window(self.parent, self)

        # Make the side panel display
        self.side_panel = QWidget()
        side_panel_layout = QVBoxLayout()
        self.side_panel.setLayout(side_panel_layout)
        self.side_panel.setFixedWidth(130)
        side_panel_layout.addWidget(self.control_widget)

        # Add items to the grid layout
        self.grid_layout.addWidget(self.side_panel, 0, 0)


def display_control_window(parent, win):
    """Makes the display control window that allows you to determine 
        what data you wish to visualize"""
    control_layout = QVBoxLayout()
    win.control_widget = QGroupBox(win, title="Display Data")
    win.control_widget.setStyleSheet(styles.roiFrameStyle())
    win.control_widget.setFont(styles.roi_btn_font())
    win.control_widget.setLayout(control_layout)
    win.control_widget.setFixedWidth(120)

    #### ADD BUTTONS ####

    # dF/F button
    win.dFoF_btn = QPushButton("dFoF")
    win.dFoF_btn.setStyleSheet(styles.roiBtnStyle())
    win.dFoF_btn.setFont(styles.roi_btn_font())
    win.dFoF_btn.clicked.connect(lambda: print("add function"))
    win.dFoF_btn.setToolTip("Display dFoF traces")
    if parent.dFoF is None:
        win.dFoF_btn.setEnabled(False)

    # Processed dFoF button
    win.processed_dFoF_btn = QPushButton("Processed dFoF")
    win.processed_dFoF_btn.setStyleSheet(styles.roiBtnStyle())
    win.processed_dFoF_btn.setFont(styles.roi_btn_font())
    win.processed_dFoF_btn.clicked.connect(lambda: print("add function"))
    win.processed_dFoF_btn.setToolTip("Display processed dFoF traces")
    if parent.processed_dFoF is None:
        win.processed_dFoF_btn.setEnabled(False)

    # estimated spikes button
    win.spikes_btn = QPushButton("Spikes")
    win.spikes_btn.setStyleSheet(styles.roiBtnStyle())
    win.spikes_btn.setFont(styles.roi_btn_font())
    win.spikes_btn.clicked.connect(lambda: print("add function"))
    win.spikes_btn.setToolTip("Display estimated spikes")
    if parent.deconvolved_spikes is None:
        win.spikes_btn.setEnabled(False)

    # volume button
    win.volume_btn = QPushButton("Volume")
    win.volume_btn.setStyleSheet(styles.roiBtnStyle())
    win.volume_btn.setFont(styles.roi_btn_font())
    win.volume_btn.clicked.connect(lambda: print("add function"))
    win.volume_btn.setToolTip("Show estimated spine volume plots")
    if parent.spine_volume is None:
        win.volume_btn.setEnabled(False)

    # Add buttons to frame
    control_layout.addWidget(win.dFoF_btn)
    control_layout.addWidget(win.processed_dFoF_btn)
    control_layout.addWidget(win.spikes_btn)
    control_layout.addWidget(win.volume_btn)
    control_layout.addStretch(1)

