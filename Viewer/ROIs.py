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
    sbr = parent.display_image.ImageEllipse.mapRectToItem(parent.current_image,br)
    print(sbr)
    sbr_rect = sbr.getRect()
    ROI_pen = pg.mkPen((76,38,212),width=4)
    parent.ellipseROI = pg.EllipseROI(pos=(sbr_rect[0],sbr_rect[1]),
                                      size=(sbr_rect[2],sbr_rect[3]),
                                      invertible=True,
                                      pen=ROI_pen,
                                      parent=parent.current_image,
                                      movable=True,
                                      rotatable=True,
                                      resizable=True,
                                      removable=True)
    parent.ellipseROI.addTranslateHandle(pos=(0.5,0.5))

        


