""" Module for the creation and handeling of 
    ROIs"""

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QTransform
from PyQt5.QtWidgets import QApplication, QColorDialog

import messages


def Draw_ROI(parent):
    """General function to handle ROI drawing"""
    parent.status_label.setText(" Ready...")
    if parent.current_ROI_type == "Background":
        new_background_roi = ROI(parent, "Background")
        parent.ROIs["Background"].append(new_background_roi)
        parent.current_ROI_type = None

    elif parent.current_ROI_type == "Soma":
        new_soma_roi = ROI(parent, "Soma")
        parent.ROIs["Soma"].append(new_soma_roi)
        parent.current_ROI_type = None

    elif parent.current_ROI_type == "Dendrite":
        new_dendrite_roi = ROI(parent, "Dendrite")
        parent.ROIs["Dendrite"].append(new_dendrite_roi)
        parent.current_ROI_type = None

    elif parent.current_ROI_type == "Spine":
        new_spine_roi = ROI(parent, "Spine")
        parent.ROIs["Spine"].append(new_spine_roi)
        parent.current_ROI_type = None


def Trigger_Background_ROI(parent, view):
    """Function to trigger background ROI drawing"""
    if parent.filename is None:
        messages.load_image_warning(parent)
    if not parent.ROIs["Background"]:
        parent.status_label.setText("Drawing Background")
        parent.current_ROI_type = "Background"
        trigger_draw_ellipse(parent, view)
    else:
        messages.background_roi_warning(parent, view)


def Trigger_Soma_ROI(parent, view):
    """Function to trigger soma ROI drawing"""
    if parent.filename is None:
        messages.load_image_warning(parent)
    parent.status_label.setText("Drawing Soma")
    parent.current_ROI_type = "Soma"
    trigger_draw_ellipse(parent, view)


def Trigger_Dendrite_ROI(parent, view):
    """Function to trigger dendrite ROI drawing"""
    if parent.filename is None:
        messages.load_image_warning(parent)
    parent.current_ROI_type = "Dendrite"
    trigger_draw_line(parent, view)


def Trigger_Spine_ROI(parent, view):
    """Function to trigger spine ROI drawing"""
    if parent.filename is None:
        messages.load_image_warning(parent)
    parent.status_label.setText("Drawing Spine")
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
    if parent.filename is not None:
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        # set mouse mode of viewbox to allow drawing
        view.setMouseMode(pg.ViewBox.RectMode)


def redraw_background(parent, view):
    """Function to redraw background"""
    parent.display_image.removeItem(parent.ROIs["Background"][0].roi)
    parent.display_image.removeItem(parent.ROIs["Background"][0].label)
    del parent.ROIs["Background"][0]
    Trigger_Background_ROI(parent, view)


def set_ROI_pen_color(parent):
    """Function to change the outline color of ROIs"""
    color = QColorDialog.getColor()
    parent.ROI_pen = pg.mkPen(color, width=4)
    for value in parent.ROIs.values():
        if not value:
            pass
        else:
            for v in value:
                print(type(v))
                v.roi.setPen(color, width=4)


def set_highlight_color(parent):
    """Function to change the highlight color of ROI when mouse hovers"""
    color = QColorDialog.getColor()
    parent.highlight_pen = pg.mkPen(color, width=4)
    for value in parent.ROIs.values():
        if not value:
            pass
        else:
            for v in value:
                v.roi.hoverPen = parent.highlight_pen


def set_selection_color(parent):
    """Function to change the ROI color when it is selected"""
    color = QColorDialog.getColor()
    parent.selection_pen = pg.mkPen(color, width=4)
    for value in parent.selected_ROIs.values():
        if not value:
            pass
        else:
            for v in value:
                v.roi.setPen = parent.selection_pen


def toggle_ROI_labels(parent):
    """Function to toggle the display of the ROI labels"""
    if parent.display_ROI_labels is True:
        for value in parent.ROIs.values():
            if not value:
                pass
            else:
                for v in value:
                    v.label.hide()
        parent.display_ROI_labels = False

    elif parent.display_ROI_labels is False:
        for value in parent.ROIs.values():
            if not value:
                pass
            else:
                for v in value:
                    v.label.show()
        parent.display_ROI_labels = True


def set_label_color(parent):
    """Function to set the ROI label color"""
    color = QColorDialog.getColor()
    parent.ROI_label_color = color
    for value in parent.ROIs.values():
        if not value:
            pass
        else:
            for v in value:
                v.label.setColor(parent.ROI_label_color)


def to_select_ROIs(parent):
    """Function to allow ROIs to be selected"""
    if parent.select_ROIs is False:
        parent.status_label.setText("Selecting ROIs")
        for value in parent.ROIs.values():
            if not value:
                pass
            else:
                for v in value:
                    v.roi.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        parent.select_ROIs = True

    elif parent.select_ROIs is True:
        parent.status_label.setText(" Ready...")
        for value in parent.ROIs.values():
            if not value:
                pass
            else:
                for v in value:
                    v.roi.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        parent.select_ROIs = False


def select_ROIs(parent, roi):
    """Function to select ROIs"""
    t = roi.type
    if roi not in parent.selected_ROIs[t]:
        roi.setPen(parent.selection_pen)
        parent.selected_ROIs[t].append(roi)
    elif roi in parent.selected_ROIs[t]:
        roi.setPen(parent.ROI_pen)
        parent.selected_ROIs[t].remove(roi)


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
            self.roi.type = self.type
        elif self.type == "Soma":
            self.roi = self.create_ellipse_roi(self.parent, self.type)
            self.roi.type = self.type
        elif self.type == "Dendrite":
            self.create_dendrite_roi()
            self.roi.type = self.type
        elif self.type == "Spine":
            self.roi = self.create_ellipse_roi(self.parent, self.type)
            self.roi.type = self.type
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
        hover_pen = parent.highlight_pen
        roi = pg.EllipseROI(
            pos=(sbr_rect[0], sbr_rect[1]),
            size=(sbr_rect[2], sbr_rect[3]),
            invertible=True,
            pen=ROI_pen,
            hoverPen=hover_pen,
            parent=parent.current_image,
            movable=True,
            rotatable=True,
            resizable=True,
            removable=True,
        )
        roi.addTranslateHandle(pos=(0.5, 0.5))
        roi.sigRegionChanged.connect(lambda: self.update_roi_label(parent, roi))
        roi.sigClicked.connect(lambda: select_ROIs(parent, roi))

        # Create ROI label
        roi_rect = roi.mapRectToParent(roi.boundingRect())
        if roi_type == "Background":
            self.label = pg.TextItem(text="BG", color=parent.ROI_label_color)
        elif roi_type == "Soma":
            length = len(parent.ROIs["Soma"])
            self.label = pg.TextItem(
                text=f"So {length+1}", color=parent.ROI_label_color
            )
        elif roi_type == "Spine":
            length = len(parent.ROIs["Spine"])
            self.label = pg.TextItem(
                text=f"Sp {length+1}", color=parent.ROI_label_color
            )
        elif roi_type == "Dendrite":
            length = len(parent.ROIs["Dendrite"])
            self.label = pg.TextItem(text=f"D {length+1}", color=parent.ROI_label_color)

        self.label.setPos(roi_rect.center())
        parent.display_image.addItem(self.label)

        return roi

    def update_roi_label(self, parent, roi):
        """Method to update ROI label position"""
        rect = roi.boundingRect()
        rect = roi.mapRectToParent(rect)
        self.label.setPos(rect.center())
