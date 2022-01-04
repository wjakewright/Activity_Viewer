""" Module for the creation and handeling of 
    ROIs"""

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QTransform
from PyQt5.QtWidgets import QApplication


class ROI:
    """Class for the creation of individual ROI objects"""

    def __init__(self, parent, type):
        self.parent = parent
        self.type = type
        self.roi = None
        self.label = None

        self.create_roi(type)

    def create_roi(self):
        """Method for the initial creation of the ROI"""
        # Assess the type of ROI to draw
        if self.type == "Background":
            self.create_background_roi()
        elif self.type == "Soma":
            self.create_soma_roi()
        elif self.type == "Dendrite":
            self.create_dendrite_roi()
        elif self.type == "Spine":
            self.create_spine_roi()
        else:
            pass

    def create_background_roi(self):
        """Method for the creation of the background ROI"""


def Trigger_Draw_ROI(parent, view):
    """Function to trigger ROI drawing"""
    # Reset cursor
    if parent.filename is not None:
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        # set mouse mode of viewbox to allow drawing
        view.setMouseMode(pg.ViewBox.RectMode)


def Draw_ROI(parent):
    """Function to draw ROI"""
    # Get coordinates of the ellipses bounding rect in the ViewBox
    br = parent.display_image.ImageEllipse.boundingRect()
    sbr = parent.display_image.ImageEllipse.mapRectToParent(br)
    center = sbr.center()
    transformer = QTransform()
    transformer.translate(center.x(), center.y()).scale(0.2, 0.2).translate(
        -center.x(), -center.y()
    )
    sbr = transformer.mapRect(sbr)
    sbr_rect = sbr.getRect()

    # Make the ROI
    ROI_pen = pg.mkPen((76, 38, 212), width=4)
    parent.ellipseROI = pg.EllipseROI(
        pos=(sbr_rect[0], sbr_rect[1]),
        size=(sbr_rect[2], sbr_rect[3]),
        invertible=True,
        pen=ROI_pen,
        parent=parent.current_image,
        movable=True,
        rotatable=True,
        resizable=True,
        removable=True,
    )
    parent.ellipseROI.addTranslateHandle(pos=(0.5, 0.5))
    rect = parent.ellipseROI.mapRectToParent(parent.ellipseROI.boundingRect())
    parent.ellipseROI.sigRegionChanged.connect(
        lambda: Update_ROI_label(parent, parent.ellipseROI)
    )
    parent.roiLabel = pg.TextItem(text="ROI", color="w")
    parent.roiLabel.setPos(rect.center())
    parent.display_image.addItem(parent.roiLabel)


def Update_ROI_label(parent, roi):
    # Updates label position when ROI is moved
    rect = roi.boundingRect()
    rect = roi.mapRectToParent(rect)
    parent.roiLabel.setPos(rect.center())
