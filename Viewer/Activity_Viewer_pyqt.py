#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItemGroup,
    QGridLayout,
    QLabel,
    QMainWindow,
    QStatusBar,
    QWidget,
)

import buttons
import display
import menus
import messages
import ROIs
import styles


class Activity_Viewer(QMainWindow):
    """GUI to label neural ROIs and extract fluorescence timecourse from 
        from two-photon imaging videos.
        
        CREATOR
            William (Jake) Wright - 11/10/2021  """

    def __init__(self):
        """Initialize class and set up some parameters """
        super(Activity_Viewer, self).__init__()

        # Set up some basic window properties
        pg.setConfigOptions(imageAxisOrder="row-major")
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.8)
        win_w = int(screen_size.width() * 0.9)
        self.setGeometry(50, 50, win_w, win_h)
        self.setStyleSheet("background:black")
        self.setWindowTitle("Activity Viewer")

        self.initUI()

    def initUI(self):
        """Creating the GUI"""
        # Initialize some attributes and parameters
        self.color_map = "Inferno"  # Default heatmap set to inferno
        self.img_threshold = 0  # Default low threshold
        self.gamma = 1
        self.image_status = "video"
        self.idx = 0
        self.default_directory = None
        self.filename = None
        self.image_directory = None
        self.tif_stack = None
        self.tif_images = []
        self.playBtnStatus = "Off"
        self.ROI_pen = pg.mkPen((255, 255, 255), width=2)
        self.highlight_pen = pg.mkPen((255, 255, 0), width=2)
        self.selection_pen = pg.mkPen((219, 3, 252), width=2)
        self.ROI_label_color = (255, 255, 255)
        self.current_ROI_type = None
        self.display_ROI_labels = True
        self.ROIs = {"Background": [], "Soma": [], "Dendrite": [], "Spine": []}
        self.select_ROIs = False
        self.shift_ROIs = False
        self.flag_ROIs = False
        self.selected_ROIs = {
            "Background": [],
            "Soma": [],
            "Dendrite": [],
            "Spine": [],
        }
        self.sensor_list = ["GCaMP6f", "GCaMP6s", "GCaMP7b", "iGluSnFr3", "RCaMP2"]
        self.imaging_sensor = "GCaMP6f"
        self.parameters = None
        self.ROI_fluorescence = None
        self.bout_separation_frames = None
        self.ROI_positions = None
        self.fluorescence_subtracted = None
        self.fluorescence_processed = None
        self.drifting_baseline = None
        self.dFoF = None
        self.processed_dFoF = None
        self.deconvolved_spikes = None
        self.spine_pixel_intensity = None
        self.spine_volume = None

        # Main menu bar
        menus.fileMenu(self)
        menus.imageMenu(self)
        menus.roiMenu(self)

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.status_label = QLabel(self)
        self.status_label.setText(" Ready...")
        self.status_bar.addWidget(self.status_label)
        self.status_label.setStyleSheet(styles.statusLabelStyle())
        self.setStatusBar(self.status_bar)

        # Setting central widget
        self.cwidget = QWidget(self)
        self.setCentralWidget(self.cwidget)

        # Grid Layout
        self.grid_layout = QGridLayout()
        self.cwidget.setLayout(self.grid_layout)

        # Buttons
        ## creates self.roi_btn_widget
        buttons.ROI_Buttons(self)

        # Image display window
        ## creates self.win, self.display_image, self.lut, self.LUT
        display.create_display(self)

        # Video timer
        self.video_timer = QtCore.QTimer(self)

        # Image view slider
        ## creates self.slider_widget
        buttons.image_slider(self)

        # Mouse position
        self.mouse_position_label = QLabel()
        self.mouse_position_label.setStyleSheet(styles.parameterLabelStyle())

        # Add widgets to MainWindow
        self.grid_layout.addWidget(self.roi_btn_widget, 0, 0)
        self.grid_layout.addWidget(self.win, 0, 1)
        self.grid_layout.addWidget(self.mouse_position_label, 1, 0)
        self.grid_layout.addWidget(self.slider_widget, 1, 1)

    def closeEvent(self, event):
        """Custom close window function"""
        messages.save_ROI_warning(self)

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Activity_Viewer()
    win.show()
    ## This if running in interactive IDE
    sys.exit(app.exec_())

