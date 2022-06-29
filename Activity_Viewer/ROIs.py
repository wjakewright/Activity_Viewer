""" Module for the creation and handeling of 
    ROIs"""

import os
import pickle
import re
import time

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from PyQt5.QtCore import QLineF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QCursor, QTransform
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QColorDialog,
    QDesktopWidget,
    QDialog,
    QFileDialog,
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsLineItem,
    QGraphicsTextItem,
    QGridLayout,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)
from shapely.geometry import LineString as ShLS
from shapely.geometry import Point as ShP

from Activity_Viewer import display, messages, styles


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
    try:
        float(parent.zoom_input.text())
    except ValueError:
        messages.zoom_warning(parent)
        return
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
    try:
        float(parent.zoom_input.text())
    except ValueError:
        messages.zoom_warning(parent)
        return
    parent.status_label.setText("Drawing Soma")
    parent.current_ROI_type = "Soma"
    trigger_draw_ellipse(parent, view)


def Trigger_Dendrite_ROI(parent, view):
    """Function to trigger dendrite ROI drawing"""
    if parent.filename is None:
        messages.load_image_warning(parent)
    try:
        float(parent.zoom_input.text())
    except ValueError:
        messages.zoom_warning(parent)
        return
    parent.status_label.setText("Drawing Dendrite (right click to end)")
    parent.current_ROI_type = "Dendrite"
    trigger_draw_line(parent, view)


def Trigger_Spine_ROI(parent, view):
    """Function to trigger spine ROI drawing"""
    if parent.filename is None:
        messages.load_image_warning(parent)
    try:
        float(parent.zoom_input.text())
    except ValueError:
        messages.zoom_warning(parent)
        return
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
    parent.ROI_pen = pg.mkPen(color, width=2)
    for key, value in parent.ROIs.items():
        if not value:
            continue
        if key != "Dendrite":
            for v in value:
                v.roi.setPen(parent.ROI_pen)
        else:
            for v in value:
                v.roi.pen = parent.ROI_pen
                for line in v.roi.drawnLine:
                    line.setPen(parent.ROI_pen)
                for r in v.roi.poly_rois:
                    r.setPen(parent.ROI_pen)


def set_highlight_color(parent):
    """Function to change the highlight color of ROI when mouse hovers"""
    color = QColorDialog.getColor()
    parent.highlight_pen = pg.mkPen(color, width=2)
    for value in parent.ROIs.values():
        if not value:
            continue
        for v in value:
            v.roi.hoverPen = parent.highlight_pen


def set_selection_color(parent):
    """Function to change the ROI color when it is selected"""
    color = QColorDialog.getColor()
    parent.selection_pen = pg.mkPen(color, width=2)
    for key, value in parent.selected_ROIs.items():
        if not value:
            continue
        if key != "Dendrite":
            for v in value:
                v.roi.setPen = parent.selection_pen
        else:
            for v in value:
                v.roi.pen = parent.selection_pen
                for line in v.roi.drawnLine:
                    line.setPen(parent.selection_pen)
                for r in v.roi.poly_rois:
                    r.setPen(parent.selection_pen)


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


def to_relable_ROIs(parent):
    """Function to relable ROIs"""
    for key in parent.ROIs.keys():
        if key == "Background":
            continue
        relable_ROIs(parent, key)


def relable_ROIs(parent, key):
    """Function that relables ROIs"""
    for i, roi in enumerate(parent.ROIs[key]):
        if key == "Soma":
            k = "So"
            roi.label.setText(f"{k} {i+1}")
        elif key == "Spine":
            k = "Sp"
            roi.label.setText(f"{k} {i+1}")
        elif key == "Dendrite":
            k = "D"
            roi.label.setPlainText(f"{k} {i+1}")


def set_label_color(parent):
    """Function to set the ROI label color"""
    color = QColorDialog.getColor()
    parent.ROI_label_color = color
    for key, value in parent.ROIs.items():
        if not value:
            continue
        if key != "Dendrite":
            for v in value:
                v.label.setColor(parent.ROI_label_color)
        else:
            for v in value:
                v.label.setDefaultTextColor(parent.ROI_label_color)


def to_delete_ROIs(parent):
    """Function to select and delete ROIs"""
    if parent.select_ROIs is False:
        parent.status_label.setText("Deleting ROIs (reclick to end)")
        for key, value in parent.ROIs.items():
            if not value:
                continue
            if key != "Dendrite":
                for v in value:
                    v.roi.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        parent.select_ROIs = True

    elif parent.select_ROIs is True:
        messages.delete_roi_warning(parent)
        for key, value in parent.ROIs.items():
            if not value:
                continue
            if key != "Dendrite":
                for v in value:
                    v.roi.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        parent.select_ROIs = False


def delete_ROIs(parent):
    """Function to finalize ROI deletion"""
    for t, rois in parent.selected_ROIs.items():
        if not rois:
            continue
        del_idx = []
        for roi in rois:
            for i, rs in enumerate(parent.ROIs[t]):
                if roi is rs:
                    del_idx.append(i)
            parent.display_image.removeItem(roi.label)
            parent.display_image.removeItem(roi.roi)
        temp_rois = [
            parent.ROIs[t][i] for i, _ in enumerate(parent.ROIs[t]) if i not in del_idx
        ]
        parent.selected_ROIs[t] = []
        parent.ROIs[t] = temp_rois
        del temp_rois
    to_relable_ROIs(parent)
    parent.status_label.setText("Ready...")


def to_flag_ROIs(parent):
    """Function to select ROIs to add flag too"""
    parent.status_label.setText("Selecting ROIs to flag")
    parent.flag_ROIs = True
    for key, value in parent.ROIs.items():
        if not value:
            continue
        if key != "Dendrite":
            for v in value:
                v.roi.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
    parent.select_ROIs = True


def flag_ROIs(parent, roi):
    """Function to add flags to ROIs"""
    flag_win = Flag_Window(parent, roi)
    flag_win.show()


def add_flags(parent, roi, win, list):
    selected_flags = list.selectedItems()
    selected_flags = [x.text() for x in selected_flags]
    for flag in selected_flags:
        if flag not in roi.flag:
            roi.flag.append(flag)
    for flag in roi.flag:
        if flag not in selected_flags:
            roi.flag.remove(flag)
    win.close()
    parent.flag_ROIs = False
    parent.select_ROIs = False
    parent.status_label.setText("Ready...")


def to_clear_ROIs(parent):
    """Function to initiate clearing all ROIs"""
    parent.status_label.setText("Clearing ROIs")
    messages.clear_roi_warning(parent)


def clear_ROIs(parent):
    """Function to clear and delete all ROIs"""
    for key, rois in parent.ROIs.items():
        for roi in rois:
            parent.display_image.removeItem(roi.label)
            parent.display_image.removeItem(roi.roi)
        parent.ROIs[key] = []
    parent.status_label.setText("Ready...")


def to_select_ROIs(parent):
    """Function to allow ROIs to be selected
        Not currently used"""
    if parent.select_ROIs is False:
        parent.status_label.setText("Selecting ROIs")
        for key, value in parent.ROIs.items():
            if not value:
                continue
            if key != "Dendrite":
                for v in value:
                    v.roi.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        parent.select_ROIs = True

    elif parent.select_ROIs is True:
        parent.status_label.setText(" Ready...")
        for key, value in parent.ROIs.items():
            if not value:
                continue
            if key != "Dendrite":
                for v in value:
                    v.roi.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        parent.select_ROIs = False


def select_ROIs(parent, roi):
    """Function to select ROIs"""
    if parent.flag_ROIs is True:
        flag_ROIs(parent, roi)
        return
    t = roi.type
    if roi not in parent.selected_ROIs[t]:
        if roi.type != "Dendrite":
            roi.roi.setPen(parent.selection_pen)
        else:
            roi.roi.pen = parent.selection_pen
            for line in roi.roi.drawnLine:
                line.setPen(parent.selection_pen)
            for r in roi.roi.poly_rois:
                r.setPen(parent.selection_pen)
        parent.selected_ROIs[t].append(roi)

    elif roi in parent.selected_ROIs[t]:
        if roi.type != "Dendrite":
            roi.roi.setPen(parent.ROI_pen)
        else:
            roi.roi.pen = parent.ROI_pen
            for line in roi.roi.drawnLine:
                line.setPen(parent.ROI_pen)
            for r in roi.roi.poly_rois:
                r.setPen(parent.ROI_pen)
        parent.selected_ROIs[t].remove(roi)


def to_shift_ROIs(parent):
    """Function to allow for all ROIs to be moved together"""
    if parent.shift_ROIs is False:
        for key, value in parent.ROIs.items():
            if key != "Dendrite":
                for v in value:
                    v.roi.rotatable = False
                    v.roi.resizable = False
        parent.status_label.setText(" Shifting ROIs")
        parent.shift_ROIs = True
    else:
        for key, value in parent.ROIs.items():
            if key != "Dendrite":
                for v in value:
                    v.roi.rotatable = True
                    v.roi.resizable = True
        parent.status_label.setText(" Ready...")
        parent.shift_ROIs = False


def shift_ROIs(parent, roi):
    """Function to shift all ROIs when one is moved"""
    if parent.shift_ROIs is True:
        if type(roi) != Dendrite_ROI:
            start = roi.preMoveState["pos"]
            curr = roi.pos()
            diff = curr - start
        else:
            start = roi.previous_position
            curr = roi.pos()
            diff = curr - start
        for key, value in parent.ROIs.items():
            if key != "Dendrite":
                for v in value:
                    if v.roi != roi:
                        v.roi.blockSignals(True)
                        v.roi.translate(diff)
                        v.update_roi_label(parent, v.roi)
                        v.roi.blockSignals(False)
            else:
                for v in value:
                    if v.roi != roi:
                        v.roi.moveBy(diff.x(), diff.y())

    else:
        pass


def save_ROIs(parent):
    # Function to save all ROIs
    save_dialog = QFileDialog()
    # save_dialog.setOptions(QFileDialog.DontUseNativeDialog)
    save_dialog.setFileMode(QFileDialog.AnyFile)
    save_dialog.setAcceptMode(QFileDialog.AcceptSave)
    save_dialog.setDirectory(r"C:\Users\Jake\Desktop\Analyzed_data\individual")
    year = time.ctime(os.path.getctime(parent.filename))[-2:]
    mouse = re.search("JW[0-9]{3}", parent.filename).group()
    date = year + re.search("[0-9]{4}", parent.filename).group()
    sname = f"{mouse}_{date}_imaging_data"
    save_dialog.selectFile(sname)
    save_dialog.show()

    if save_dialog.exec() == QFileDialog.Accepted:
        save_name = save_dialog.selectedFiles()[0]
        pickle_name = save_name + ".rois"
        rois = {"Background": [], "Soma": [], "Dendrite": [], "Spine": []}
        for key, value in parent.ROIs.items():
            if key != "Dendrite":
                for v in value:
                    state = v.roi.saveState()
                    rois[key].append(state)
            else:
                r = {"Points": [], "Del": []}
                for v in value:
                    points = v.roi.points
                    r["Points"] = points
                    r["Del"] = v.roi.del_idxs
                rois[key].append(r)
        with open(pickle_name, "wb") as f:
            pickle.dump(rois, f)

        # Export the image
        image_name = save_name + ".png"
        exporter = pg.exporters.ImageExporter(parent.display_image)
        exporter.export(image_name)


def load_ROIs(parent):
    # Function to load ROIs
    if parent.tif_stack is None:
        messages.load_image_warning(parent)

    load_name = QFileDialog.getOpenFileName(parent, "Load ROIs")[0]
    with open(load_name, "rb") as f:
        load_rois = pickle.load(f)

    for key, value in load_rois.items():
        roi_type = key
        if key != "Dendrite":
            for v in value:
                roi = ROI(parent, roi_type)
                roi.roi.setState(v)
                parent.ROIs[roi_type].append(roi)
        else:
            for v in value:
                roi = ROI(parent, roi_type, v["Points"])
                roi.roi.del_poly_load(v["Del"])
                parent.ROIs[roi_type].append(roi)


class ROI:
    """Class for the creation of individual ROI objects"""

    def __init__(self, parent, roi_type, loading=False):
        self.parent = parent
        self.type = roi_type
        self.loading = loading
        self.roi = None
        self.label = None
        self.start_pos = None
        self.flag = []

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
            self.roi = self.create_poly_line(self.parent, self.type)
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
        roi.sigRegionChangeFinished.connect(lambda: shift_ROIs(parent, roi))
        roi.sigClicked.connect(lambda: select_ROIs(parent, self))

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

        self.label.setPos(roi_rect.center())
        parent.display_image.addItem(self.label)

        return roi

    def create_poly_line(self, parent, roi_type):
        """Method to create poly line ROI for dendrites"""
        ROI_pen = parent.ROI_pen
        hover_pen = parent.highlight_pen

        # Create ROI
        if self.loading is False:
            roi = Dendrite_ROI(
                points=parent.display_image.LinePoints,
                GUI=parent,
                parent_ROI=self,
                parent=parent.current_image,
                pen=ROI_pen,
                hovepen=hover_pen,
            )
        else:
            roi = Dendrite_ROI(
                points=self.loading,
                GUI=parent,
                parent_ROI=self,
                parent=parent.current_image,
                pen=ROI_pen,
                hovepen=hover_pen,
            )

        roi.setAcceptHoverEvents(True)

        # Create ROI label
        length = len(parent.ROIs["Dendrite"])
        self.label = QGraphicsTextItem(f"D {length+1}")
        self.label.setDefaultTextColor(QColor(*parent.ROI_label_color))
        roi.addToGroup(self.label)
        pos_index = int(len(roi.drawn_lines) // 2)
        self.label.setPos(roi.drawn_lines[pos_index].p1())

        return roi

    def update_roi_label(self, parent, roi):
        """Method to update ROI label position"""
        rect = roi.boundingRect()
        rect = roi.mapRectToParent(rect)
        self.label.setPos(rect.center())


class Dendrite_ROI(QGraphicsItemGroup):
    """Custom Dendrite ROI. Container to hold multiple ellipse rois along
        the length of the drawn dendrite"""

    sigRegionChangeFinished = pyqtSignal(object)
    sigRegionChangeStarted = pyqtSignal(object)
    sigRegionChanged = pyqtSignal(object)

    def __init__(self, points, GUI, parent_ROI, parent, pen, hovepen, loading=False):
        """Takes a list of QPointFs in order to generate a shapely line
            for the dendrite. This line is then stored and used to generate
            the individual ellipse ROIs along the dendrite"""
        super(Dendrite_ROI, self).__init__(parent=parent)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemStacksBehindParent, False)

        self.points = points
        self.GUI = GUI
        self.parent_ROI = parent_ROI
        self.parent = parent
        self.pen = pen
        self.hoverPen = hovepen
        self.poly_rois = []
        self.line = None
        self.drawn_lines = []
        self.drawnLine = []
        self.del_idxs = []
        self.previous_position = None

        self.selected_polys = []

        self.create_line()
        self.draw_line()
        self.create_rois()

    def paint(self, painter, *args, **kwargs):
        # Need to override the original abstract method
        pass

    def mouseReleaseEvent(self, event):
        """Reimplementation of mouse move event"""
        # Call the original function
        QGraphicsItemGroup.mouseReleaseEvent(self, event)
        # Additional functionality
        shift_ROIs(self.GUI, self)

    def mousePressEvent(self, event):
        """Reimplementing the mouse press event for additional function"""
        self.previous_position = self.pos()
        if event.buttons() & Qt.LeftButton:
            if self.GUI.select_ROIs is False:
                QGraphicsItemGroup.mousePressEvent(self, event)
            else:
                select_ROIs(self.GUI, self.parent_ROI)
                QGraphicsItemGroup.mousePressEvent(self, event)
        elif event.buttons() & Qt.RightButton:
            self.poly_win = Poly_ROI_Window(self.GUI, self.parent_ROI)
            self.poly_win.show()

    def hoverEnterEvent(self, event):
        self.paint_hover_color()
        self.update()

    def hoverLeaveEvent(self, event):
        self.wash_hover_color()
        self.update()

    def create_line(self):
        """Creates shapely line from QPointFs"""
        shapely_points = []
        for point in self.points:
            s_point = ShP(point.x(), point.y())
            shapely_points.append(s_point)
        self.line = ShLS(shapely_points)

    def draw_line(self):
        """Function to draw line"""
        for i, p in enumerate(self.points[:-1]):
            self.drawn_lines.append(QLineF(p, self.points[i + 1]))
        for line in self.drawn_lines:
            drawnLine = QGraphicsLineItem(line, parent=self)
            drawnLine.setAcceptHoverEvents(True)
            drawnLine.setPen(self.pen)
            self.drawnLine.append(drawnLine)

    def create_rois(self):
        """Creates individual ellipse rois along the length of the dendrite line"""
        # Constants for ROI size and spacing inbetween
        ROI_SIZE = 0.5  # um
        ROI_SPACE = 1  # um
        # Get conversion factors between pixels and um
        pix_conv = display.convert_pixels_to_um(self.GUI)
        # Get size and spacing of ROIs in pixels
        roi_size = ROI_SIZE * pix_conv
        roi_spacing = ROI_SPACE * pix_conv
        # Get the positions of rois to make along the line
        roi_pos = np.linspace(0, self.line.length, int(self.line.length // roi_spacing))
        # Make the ROIs
        for p in roi_pos:
            pos = self.line.interpolate(p)
            x = pos.x - (roi_size / 2)
            y = pos.y - (roi_size / 2)
            new_roi = pg.EllipseROI(
                pos=(x, y),
                size=(roi_size, roi_size),
                pen=self.pen,
                parent=self,
                hoverPen=self.hoverPen,
                rotatable=False,
            )
            # new_roi.sigRegionChanged.connect(lambda:self.translate_rois())
            new_roi.translatable = False
            new_roi.removeHandle(0)
            new_roi.removeHandle(0)
            self.poly_rois.append(new_roi)

    def highlight_poly(self, roi):
        """Function to highlight individual poly rois when selecting for deleting"""
        self.wash_hover_color()
        idx = int(roi.text().split(" ")[1]) - 1
        if idx not in self.selected_polys:
            self.selected_polys.append(idx)
        else:
            self.selected_polys.remove(idx)

        for i in self.selected_polys:
            self.poly_rois[i].setPen(self.GUI.selection_pen)
        self.update()

    def del_poly(self, list):
        """Function to delete selected poly ROIs"""
        idxs = [int(roi.text().split(" ")[1]) - 1 for roi in list.selectedItems()]
        self.del_idxs = idxs
        for i in idxs:
            self.GUI.display_image.removeItem(self.poly_rois[i])
        self.poly_rois = [
            self.poly_rois[i] for i, _ in enumerate(self.poly_rois) if i not in idxs
        ]

        self.poly_win.close()

    def del_poly_load(self, idxs):
        """Function to delete poly rois that were previously deleted"""
        for i in idxs:
            self.GUI.display_image.removeItem(self.poly_rois[i])
        self.poly_rois = [
            self.poly_rois[i] for i, _ in enumerate(self.poly_rois) if i not in idxs
        ]

    def paint_hover_color(self):
        """Function allow for over color change over the ROI"""
        for line in self.drawnLine:
            line.setPen(self.hoverPen)
        for roi in self.poly_rois:
            roi.setPen(self.hoverPen)

    def wash_hover_color(self):
        """Function to revert pen color after hovering done"""
        for line in self.drawnLine:
            line.setPen(self.pen)
        for roi in self.poly_rois:
            roi.setPen(self.pen)


class Poly_ROI_Window(QDialog):
    """Custom window to display a list of poly rois that will allow you to delete them"""

    def __init__(self, parent, roi):
        super(Poly_ROI_Window, self).__init__(parent=parent)
        self.parent = parent
        self.roi = roi

        screen_size = QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.5)
        win_w = int(screen_size.width() * 0.1)
        self.setGeometry(150, 150, win_w, win_h)
        self.setStyleSheet("border: 3px solid #132743")
        self.setWindowTitle("Poly ROIs")

        self.initWindow()

    def initWindow(self):
        """Initialize the window"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Make the list
        self.poly_roi_list = QListWidget()
        self.poly_roi_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.poly_roi_list.setStyleSheet(styles.roiListStyle())
        poly_rois = self.roi.roi.poly_rois
        for roi in range(len(poly_rois)):
            label = f"ROI {roi+1}"
            item = QListWidgetItem(label)
            self.poly_roi_list.addItem(item)
        self.poly_roi_list.itemClicked.connect(lambda x: self.roi.roi.highlight_poly(x))

        # Make the delete button
        self.del_btn = QPushButton("Delete")
        self.del_btn.setStyleSheet(styles.roiBtnStyle())
        self.del_btn.setFont(styles.roi_btn_font())
        self.del_btn.clicked.connect(lambda: self.roi.roi.del_poly(self.poly_roi_list))
        self.del_btn.setToolTip("Delete selected Poly ROIs")

        self.layout.addWidget(self.poly_roi_list)
        self.layout.addWidget(self.del_btn)


class Flag_Window(QDialog):
    """Custom window to add and remove flags from rois"""

    def __init__(self, parent, roi):
        super(Flag_Window, self).__init__(parent=parent)
        self.parent = parent
        self.roi = roi
        self.flags = ["New Spine", "Eliminated Spine", "Shaft Spine"]

        self.setStyleSheet("border: 3px solid #132743")
        self.setWindowTitle("ROI Flags")

        self.initWindow()

    def initWindow(self):
        """Initialize the window"""
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        roi_flags = self.roi.flag
        # Make the list
        self.flag_list = QListWidget()
        self.flag_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.flag_list.setStyleSheet(styles.roiListStyle())
        self.flag_list.setFixedWidth(150)
        for flag in self.flags:
            label = flag
            item = QListWidgetItem(label)
            self.flag_list.addItem(item)

        for flag in roi_flags:
            item = self.flag_list.findItems(flag, Qt.MatchExactly)
            if item:
                item[0].setSelected(True)

        # Make the flag button
        self.flag_btn = QPushButton("Flag ROIs")
        self.flag_btn.setStyleSheet(styles.roiBtnStyle())
        self.flag_btn.setFont(styles.roi_btn_font())
        self.flag_btn.clicked.connect(
            lambda: add_flags(self.parent, self.roi, self, self.flag_list)
        )
        self.flag_btn.setToolTip("Add selected flags")

        # Make Cancel Button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(styles.roiBtnStyle())
        self.cancel_btn.setFont(styles.roi_btn_font())
        self.cancel_btn.clicked.connect(lambda: self.close_win())
        self.cancel_btn.setToolTip("Cancel adding flag")

        self.layout.addWidget(self.flag_list, 0, 0, 1, 2)
        self.layout.addWidget(self.flag_btn, 1, 0)
        self.layout.addWidget(self.cancel_btn, 1, 1)

    def close_win(self):
        self.parent.flag_ROIs = False
        self.parent.select_ROIs = False
        self.parent.status_label.setText("Ready...")
        self.close()
