#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QScrollBar, QSizePolicy, QVBoxLayout, QWidget, QApplication, QMainWindow, QLabel, 
                             QFileDialog, QGroupBox)
# Import package specific modules
import menus 
import images


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
        self.stylePressed = ("QPushButton {Text-align: left; "
                             "background-color: rgb(55,55,138); "
                             "color:white;}")
        self.styleUnpressed = ("QPushButton {Text-align: left; "
                               "background-color: rgb(50,50,50); "
                               "color:white;}")
        self.styleInactive = ("QPushButton {Text-align: left; "
                              "background-color: rgb(120,120,120); "
                              "color:gray;}")
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
        self.tif_images = None

        # Main menu bar
        menus.fileMenu(self)
        menus.imageMenu(self)

        # Setting central widget
        self.cwidget = QWidget(self)
        self.setCentralWidget(self.cwidget)

        # Grid Layout
        self.grid_layout = QGridLayout()
        self.cwidget.setLayout(self.grid_layout)
        self.vbox_layout = QVBoxLayout()

        # Frames
        self.ROI_btn_box = QGroupBox(self,title='Manage ROIs')
        self.ROI_btn_box.setStyleSheet('background:black;color:white;border:2px solid #132743')
        self.ROI_btn_box.setLayout(self.vbox_layout)
        
        # Image display window
        self.win = pg.GraphicsLayoutWidget(self)
        self.display_image = self.win.addPlot(title="FULL VIEW",row=0,col=0)
        self.display_image.setAspectLocked(True)
        self.lut = pg.HistogramLUTItem()
        self.LUT = self.win.addItem(self.lut)
        
        

        # Image view slider
        self.image_slider = QScrollBar(Qt.Horizontal)
        self.image_slider.setFocusPolicy(Qt.StrongFocus)
        #self.image_slider.setTickPosition(QScrollBar.TicksBothSides)
        self.image_slider.setStyleSheet('''QScrollBar:horizontal {background-color:#131416;
                                                                  border: 1px solid #24272D;
                                                                  margin:0px 20px 0px 20px}
                                           QScrollBar::handle:horizontal {background:#24272D;
                                                                          color:white}
                                           QScrollBar::add-line:horizontal {background:#24272D;
                                                                            width:15px;
                                                                            subcontrol-position: right;
                                                                            subcontrol-origin: margin}
                                           QScrollBar::sub-line:horizontal {background:#24272D;
                                                                            width:15px;
                                                                            subcontrol-position: left;
                                                                            subcontrol-origin: margin}
                                           QScrollBar:left-arrow:horizontal,QScrollBar:right-arrow:horizontal{
                                                                            width:3px;
                                                                            height:3px;
                                                                            background:white}''')

        # Add widgets to MainWindow
        self.grid_layout.addWidget(self.ROI_btn_box,0,0)
        self.grid_layout.addWidget(self.win,0,1)
        self.grid_layout.addWidget(self.image_slider,1,1)
        

    def Load_file(self):
        # Get the filename
        filename = QFileDialog.getOpenFileName(self, 'Open File')[0]
        self.filename = filename
        # Load the image stack
        ## set_display_images will set self.tif_images
        images.set_display_image(self,filename)

    def Display_Image(self):
        if self.tif_images is None:
            self.Load_file()
        self.current_image = pg.ImageItem(self.tif_images[0],boarder='w')
        self.display_image.addItem(self.current_image)
        self.lut.setImageItem(self.current_image)
        self.image_slider.setMinimum(0)
        self.image_slider.setMaximum(len(self.tif_images)-1)
        self.image_slider.valueChanged.connect(self.Slider_Update_Video)
    
    def Slider_Update_Video(self):
        self.level = self.lut.getLevels()
        self.idx = self.image_slider.value()
        self.current_image.setImage(self.tif_images[self.idx])
        self.lut.setLevels(self.level[0],self.level[1])

    def stretch_image(self):
        self.display_image.setAspectLocked(False)

    def square_image(self):
        self.display_image.setAspectLocked(True)
        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Activity_Viewer()
    win.show()
    ## This if running in interactive IDE
    sys.exit(app.exec_()) 
    