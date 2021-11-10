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
        
        self.setGeometry(200,200,200,200)
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
    