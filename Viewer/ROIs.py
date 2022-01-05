""" Module for the creation and handeling of 
    ROIs"""

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QTransform
from PyQt5.QtWidgets import QApplication, QMessageBox


def Draw_ROI(parent):
    """General function to handle ROI drawing"""
    if parent.current_ROI_type == "Background":
        new_background_roi = ROI(parent, "Background")
        parent.ROIs["Background"].append(new_background_roi)
        parent.current_ROI_type = None

    elif parent.current_ROI_type == "Soma":
        new_soma_roi = ROI(parent, "Soma").roi
        parent.ROIs["Somas"].append(new_soma_roi)
        parent.current_ROI_type = None

    elif parent.current_ROI_type == "Dendrite":
        new_dendrite_roi = ROI(parent, "Dendrite")
        parent.ROIs["Dendrites"].append(new_dendrite_roi)
        parent.current_ROI_type = None

    elif parent.current_ROI_type == "Spine":
        new_spine_roi = ROI(parent, "Spine")
        parent.ROIs["Spines"].append(new_spine_roi)
        parent.current_ROI_type = None


def Trigger_Background_ROI(parent, view):
    """Function to trigger background ROI drawing"""
    if not parent.ROIs["Background"]:
        parent.current_ROI_type = "Background"
        trigger_draw_ellipse(parent, view)
    else:
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText("Background Already Drawn")
        warning.setWindowTitle("Background Warning")
        warning.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = warning.exec()


def Trigger_Soma_ROI(parent, view):
    """Function to trigger soma ROI drawing"""
    parent.current_ROI_type = "Soma"
    trigger_draw_ellipse(parent, view)


def Trigger_Dendrite_ROI(parent, view):
    """Function to trigger dendrite ROI drawing"""
    parent.current_ROI_type = "Dendrite"
    # trigger_draw_line(parent,view)  ## Need to code this part into the rest of the GUI


def Trigger_Spine_ROI(parent, view):
    """Function to trigger spine ROI drawing"""
    parent.current_ROI_type = "Spine"
    trigger_draw_ellipse(parent, view)


def trigger_draw_ellipse(parent, view):
    """Function to trigger ellipse drawing upon mouse drag"""
    if parent.filename is not None:
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        # set mouse mode of viewbox to allow drawing
        view.setMouseMode(pg.ViewBox.RectMode)


def trigger_draw_line(parent, view):
    """Function to trigger line drawing upon mouse clicking"""


class ROI:
    """Class for the creation of individual ROI objects"""

    def __init__(self, parent, roi_type):
        self.parent = parent
        self.type = roi_type
        self.roi = None
        self.label = None

        self.create_roi()

    def create_roi(self):
        """Method for the initial creation of the ROI"""
        # Assess the type of ROI to draw
        if self.type == "Background":
            self.roi = self.create_ellipse_roi(self.parent, self.type)
        elif self.type == "Soma":
            self.roi = self.create_ellipse_roi(self.parent, self.type)
        elif self.type == "Dendrite":
            self.create_dendrite_roi()
        elif self.type == "Spine":
            self.roi = self.create_ellipse_roi(self.parent, self.type)
        else:
            pass

    def create_ellipse_roi(self, parent, roi_type):
        """Method for the creation of the elliptical ROI"""
        # Get coordinates of the ellipse's bounding rect in ViewBox
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
        ROI_pen = parent.ROI_pen
        roi = pg.EllipseROI(
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
        roi.addTranslateHandle(pos=(0.5, 0.5))
        roi.sigRegionChanged.connect(lambda: self.update_roi_label(parent, roi))

        # Create ROI label
        roi_rect = roi.mapRectToParent(roi.boundingRect())
        if roi_type == "Background":
            self.label = pg.TextItem(text="BG", color=parent.ROI_label_color)
        elif roi_type == "Soma":
            length = len(parent.ROIs["Somas"])
            self.label = pg.TextItem(
                text=f"So {length+1}", color=parent.ROI_label_color
            )
        elif roi_type == "Spine":
            length = len(parent.ROIs["Spines"])
            self.label = pg.TextItem(
                text=f"Sp {length+1}", color=parent.ROI_label_color
            )
        elif roi_type == "Dendrite":
            length = len(parent.ROIs["Dendrites"])
            self.label = pg.TextItem(text=f"D {length+1}", color=parent.ROI_label_color)

        self.label.setPos(roi_rect.center())
        parent.display_image.addItem(self.label)

        return roi

    def update_roi_label(self, parent, roi):
        """Method to update ROI label position"""
        rect = roi.boundingRect()
        rect = roi.mapRectToParent(rect)
        self.label.setPos(rect.center())
