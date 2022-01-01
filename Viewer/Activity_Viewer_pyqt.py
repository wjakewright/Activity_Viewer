#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

import buttons
import display

# Import package specific modules
import menus


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
        self.image_size = (500, 500)  # Need to make this adjustable to windowsize
        self.image_status = "video"
        self.idx = 0
        self.filename = None
        self.tif_stack = None
        self.tif_images = []
        self.playBtnStatus = "Off"

        # Main menu bar
        menus.fileMenu(self)
        menus.imageMenu(self)

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

        # Add widgets to MainWindow
        self.grid_layout.addWidget(self.roi_btn_widget, 0, 0)
        self.grid_layout.addWidget(self.win, 0, 1)
        self.grid_layout.addWidget(self.slider_widget, 1, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Activity_Viewer()
    win.show()
    ## This if running in interactive IDE
    sys.exit(app.exec_())

