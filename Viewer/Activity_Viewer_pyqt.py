#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QScrollBar, QWidget, 
                             QApplication, QMainWindow, QFileDialog,QPushButton)
# Import package specific modules
import menus 
import images
import buttons
import styles

class Activity_Viewer(QMainWindow):
    '''GUI to label neural ROIs and extract fluorescence timecourse from 
        from two-photon imaging videos.
        
        CREATOR
            William (Jake) Wright - 11/10/2021  ''' 
            
    def __init__(self):
        '''Initialize class and set up some parameters '''
        super(Activity_Viewer,self).__init__()
        
        # Set up some basic window properties
        pg.setConfigOptions(imageAxisOrder="row-major")
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.8)
        win_w = int(screen_size.width() * 0.9)
        self.setGeometry(50,50,win_w,win_h)
        self.setStyleSheet('background:black')
        self.setWindowTitle('Activity Viewer')
        
        self.initUI()
        
    def initUI(self):
        '''Creating the GUI'''
        # Initialize some attributes and parameters
        self.color_map = 'Inferno' # Default heatmap set to inferno
        self.img_threshold = 0 # Default low threshold
        self.gamma = 1
        self.image_size = (500,500) # Need to make this adjustable to windowsize
        self.image_status = 'video'
        self.idx = 0
        self.tif_stack = None
        self.tif_images = []
        self.playBtnStatus = 'Off'

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
        buttons.ROI_Buttons(self)

        # Image display window
        self.win = pg.GraphicsLayoutWidget(self)
        self.display_image = self.win.addPlot(title="FULL VIEW",row=0,col=0)
        self.display_image.setAspectLocked(True)
        self.lut = pg.HistogramLUTItem()
        self.LUT = self.win.addItem(self.lut)

        # Video timer
        self.video_timer = QtCore.QTimer(self)

        # Image view slider
        self.slider_widget = QWidget(self)
        slider_layout = QHBoxLayout()
        self.slider_widget.setLayout(slider_layout)
        self.play_btn = QPushButton('➤')
        self.play_btn.setStyleSheet(styles.playBtnStyle())
        self.play_btn.setMaximumWidth(30)
        self.play_btn.clicked.connect(lambda: self.play_video())
        self.image_slider = QScrollBar(Qt.Horizontal)
        self.image_slider.setFocusPolicy(Qt.StrongFocus)
        self.image_slider.setStyleSheet(styles.sliderStyle())
        slider_layout.addWidget(self.play_btn)
        slider_layout.addWidget(self.image_slider)
        self.image_slider.setEnabled(False)
        self.play_btn.setEnabled(False)


        # Add widgets to MainWindow
        self.grid_layout.addWidget(self.roi_btn_widget,0,0)
        self.grid_layout.addWidget(self.win,0,1)
        self.grid_layout.addWidget(self.slider_widget,1,1)
        

    def Load_file(self):
        # Load and display image
        filename = QFileDialog.getOpenFileName(self, 'Open File')[0]
        self.filename = filename
        # Load the image stack
        ## set_display_images will set self.tif_images
        images.set_display_image(self,filename)
        # Toggle status of slider and play btn
        self.image_slider.setEnabled(True)
        self.play_btn.setEnabled(True)
        # Generate display image
        self.current_image = pg.ImageItem(self.tif_images[0],boarder='w')
        self.display_image.addItem(self.current_image)
        self.lut.setImageItem(self.current_image)
        # Set slider range
        self.image_slider.setMinimum(0)
        self.image_slider.setMaximum(len(self.tif_images)-1)
        self.image_slider.valueChanged.connect(self.Slider_Update_Video)
    
    def Slider_Update_Video(self):
        # Update displayed image when slider is moved
        self.level = self.lut.getLevels()
        self.idx = self.image_slider.value()
        self.current_image.setImage(self.tif_images[self.idx])
        self.lut.setLevels(self.level[0],self.level[1])

    def stretch_image(self):
        # Stretch the image to fill space
        self.display_image.setAspectLocked(False)

    def square_image(self):
        # Lock image in square aspect ratio
        self.display_image.setAspectLocked(True)

    def play_video(self):
        # Play the video of tif images
        if self.playBtnStatus == 'Off':
            self.video_timer.timeout.connect(lambda: self.play_update())
            self.playBtnStatus = 'On'
            self.video_timer.start(100)
            self.play_update()
        else:
            self.playBtnStatus = 'Off'
            self.video_timer.stop()
    
    def play_update(self):
        # Updates display image while playing video
        if self.idx < len(self.tif_images)-1:
            self.idx = self.idx + 1
        else:
            self.idx = 0
        self.level = self.lut.getLevels()
        self.image_slider.setValue(self.idx)
        self.current_image.setImage(self.tif_images[self.idx])
        self.lut.setLevels(self.level[0],self.level[1])
        


        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Activity_Viewer()
    win.show()
    ## This if running in interactive IDE
    sys.exit(app.exec_()) 
    