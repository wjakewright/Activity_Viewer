#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets as Widgets
from PyQt5.QtWidgets import QApplication, QMainWindow



class Activity_Viewer(QMainWindow):
    '''GUI to label neural ROIs and extract fluorescence timecourse from 
        from two-photon imaging videos.
        
        CREATOR
            William (Jake) Wright - 11/10/2021  ''' 
            
    def __init__(self):
        super(Activity_Viewer,self).__init__()
        
        # Set up some window properties
        screen_size = Widgets.QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.8)
        win_w = int(screen_size.width() * 0.9)
        self.setGeometry(50,50,win_w,win_h)
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
    