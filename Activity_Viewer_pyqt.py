#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from . import menus 




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
        
        

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Activity_Viewer()
    win.show()
    ## This if running in interactive IDE
    ## Change to sys.exit(app.exec_()) for running from command line
    app.exec_()
    