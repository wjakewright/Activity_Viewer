#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QLabel, 
                             QFileDialog)
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

        # Default image parameters
        self.color_map = 'Inferno' # Default heatmap set to inferno
        self.img_threshold = 50 # Default low threshold
        self.gamma = 1
        self.image_size = (500,500) # Need to make this adjustable to windowsize

        self.initUI()
        
    def initUI(self):
        '''Creating the GUI'''
        # Initialize some attributes
        self.filename = 'none'
        # Main menu bar
        menus.fileMenu(self)
        menus.imageMenu(self)
        
        self.label = QLabel(self)
        self.label.setStyleSheet('''QLabel {background-color: white;
                                             color:grey;}''')
        self.label.move(100,100)
        self.label.setText(str(self.filename))


    def Load_file(self):
        # Get the filename
        filename = QFileDialog.getOpenFileName(self, 'Open File')[0]
        self.filename = filename
        # Load the image stack
        ## set_display_images will set self.tif_images
        images.set_display_image(self,filename)




        

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Activity_Viewer()
    win.show()
    ## This if running in interactive IDE
    sys.exit(app.exec_()) 
    