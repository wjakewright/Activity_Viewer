''' Module for the creation and handeling of 
    ROIs'''


import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

def Trigger_Draw_ROI(parent):
    '''Function to trigger ROI drawing'''
    # Reset cursor
    QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
    # set mouse mode of viewbox to allow drawing
    parent.setMouseMode(pg.ViewBox.RectMode)

def Draw_ROI(parent):
    '''Function to draw ROI'''
    # Get coordinates of the ellipses bounding rect in the ViewBox
    br = parent.display_image.ImageEllipse.boundingRect()
    sbr = parent.display_image.ImageEllipse.mapRectToParent(br)
    

        


