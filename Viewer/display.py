""" Module containing functions for generating and updating
    the image display
    
    CREATOR
        William (Jake) Wright - 12/27/2021"""

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QTransform, QColor
from PyQt5.QtWidgets import QApplication, QFileDialog, QGraphicsEllipseItem

import images
import ROIs


def create_display(parent):
    parent.win = pg.GraphicsLayoutWidget(parent)
    parent.display_image = ImageViewBox(parent)
    # parent.display_image = parent.win.addViewBox(name='Main Image',row=0,col=0)
    parent.win.addItem(parent.display_image, row=0, col=0)
    parent.display_image.setAspectLocked(True)
    parent.lut = pg.HistogramLUTItem()
    parent.LUT = parent.win.addItem(parent.lut)


def Load_File(parent):
    # Load and display image
    filename = QFileDialog.getOpenFileName(parent, "Open File")[0]
    parent.filename = filename
    # Load the image stack
    ## Generates parent.tif_images
    images.set_display_image(parent, filename)
    # Toggle status of slider and play button
    parent.image_slider.setEnabled(True)
    parent.play_btn.setEnabled(True)
    # Generate display image
    parent.current_image = pg.ImageItem(parent.tif_images[0], border="w")
    parent.display_image.addItem(parent.current_image)
    parent.lut.setImageItem(parent.current_image)
    # Set slider range
    parent.image_slider.setMinimum(0)
    parent.image_slider.setMaximum(len(parent.tif_images) - 1)
    parent.image_slider.valueChanged.connect(lambda: Slider_Update_Video(parent))


def Stretch_Image(parent):
    # Stretch the image to fill the space
    parent.display_image.setAspectLocked(False)


def Square_Image(parent):
    # Lock image in square aspect ratio
    parent.display_image.setAspectLocked(True)


def Slider_Update_Video(parent):
    # Update displayed image when slider is moved
    parent.level = parent.lut.getLevels()
    parent.idx = parent.image_slider.value()
    parent.current_image.setImage(parent.tif_images[parent.idx])
    parent.lut.setLevels(parent.level[0], parent.level[1])


def Play_Video(parent):
    # Play the video of tif images
    if parent.playBtnStatus == "Off":
        parent.video_timer.timeout.connect(lambda: Play_Update(parent))
        parent.playBtnStatus = "On"
        parent.video_timer.start(100)
        Play_Update(parent)
    else:
        parent.playBtnStatus = "Off"
        parent.video_timer.stop()


def Play_Update(parent):
    # Updates display image while playing video
    if parent.idx < len(parent.tif_images) - 1:
        parent.idx = parent.idx + 1
    else:
        parent.idx = 0
    parent.level = parent.lut.getLevels()
    parent.image_slider.setValue(parent.idx)
    parent.current_image.setImage(parent.tif_images[parent.idx])
    parent.lut.setLevels(parent.level[0], parent.level[1])


class ImageViewBox(pg.ViewBox):
    """Custom ViewBox class to display image in.
        Allows mouse click and drag events to be toggled"""

    def __init__(self, parent, *args, **kwargs):
        super(ImageViewBox, self).__init__(*args, **kwargs)
        self.parent = parent

        # Custom Ellipse object to aid in ROI drawing
        self.ImageEllipse = QGraphicsEllipseItem(0, 0, 1, 1)
        self.ImageEllipse.setPen(pg.mkPen((240, 134, 5), width=4))
        self.ImageEllipse.setZValue(1e9)
        self.ImageEllipse.hide()
        self.addItem(self.ImageEllipse, ignoreBounds=True)

        # Points and line to aid in ROI drawing
        self.ImagePoints = []
        self.ImageLine = None

    def UpdateEllipse(self, p1, p2):
        rect = QRectF(p1, p2)
        # Ensure ellipse edge is snapped to cursor
        h = rect.height()
        w = rect.width()
        x1 = p1[0] - 0.14647 * w
        y1 = p1[1] - 0.14647 * h
        x2 = p2[0] + 0.14647 * w
        y2 = p2[1] + 0.14647 * h
        np1 = QPointF(x1, y1)
        np2 = QPointF(x2, y2)
        r = QRectF(np1, np2)
        r = self.childGroup.mapRectFromScene(r)
        self.ImageEllipse.setPos(r.topLeft())
        trScale = QTransform.fromScale(r.width(), r.height())
        self.ImageEllipse.setTransform(trScale)
        self.ImageEllipse.update()
        self.ImageEllipse.show()

    def MakePoint(self, pos):
        points = self.childGroup.mapFromScene(pos)
        point = QGraphicsEllipseItem(points.x(), points.y(), 1, 1)
        point.setPen(pg.mkPen((240, 134, 5), width=4))
        point.setBrush(QColor(240, 134, 5))
        point.setOpacity(1.0)
        point.setZValue(1e9)
        # point.hide()
        self.addItem(point, ignoreBounds=True)
        point.show()
        self.ImagePoints.append(point)

    def mouseDragEvent(self, ev, axis=None):
        # Custom mouseDragEvent method
        if (
            self.state["mouseMode"] == pg.ViewBox.RectMode
            and self.parent.current_ROI_type != "Dendrite"
        ):
            # print('Drag being triggered')
            ev.accept()
            pos = ev.pos()
            dif = (pos - ev.lastPos()) * -1
            mouseEnabled = np.array(self.state["mouseEnabled"], dtype=np.float)
            mask = mouseEnabled.copy()
            if ev.button() & Qt.LeftButton:
                if ev.isFinish():
                    self.ImageEllipse.hide()
                    QApplication.restoreOverrideCursor()
                    self.setMouseMode(pg.ViewBox.PanMode)
                    ROIs.Draw_ROI(self.parent)

                else:
                    self.UpdateEllipse(
                        ev.buttonDownScenePos(ev.button()), ev.scenePos()
                    )

        elif (
            self.state["mouseMode"] == pg.ViewBox.RectMode
            and self.parent.current_ROI_type == "Dendrite"
        ):
            ev.accept()
            pos = ev.pos()
            dif = (pos - ev.lastPos()) * -1
            mouseEnabled = np.array(self.state["mouseEnabled"], dtype=np.float)
            mask = mouseEnabled.copy()
            tr = self.childGroup.transform()
            tr = c_invertQTransform(tr)
            tr = tr.map(dif * mask) - tr.map(QPointF(0, 0))

            x = tr.x() if mask[0] == 1 else None
            y = tr.y() if mask[1] == 1 else None

            self._resetTarget()
            if x is not None or y is not None:
                self.translateBy(x=x, y=y)
            self.sigRangeChangedManually.emit(self.state["mouseEnabled"])

        else:
            super(ImageViewBox, self).mouseDragEvent(ev)

    def mouseClickEvent(self, ev):
        # Custom mouseClickedEvent method
        if (
            self.state["mouseMode"] == pg.ViewBox.RectMode
            and self.parent.current_ROI_type == "Dendrite"
        ):
            if ev.button() == Qt.MouseButton.LeftButton:
                ev.accept()
                pos = ev.scenePos()
                print(pos)
                self.MakePoint(pos)

        else:
            super(ImageViewBox, self).mouseClickedEvent(ev)


## Helper function for the custom image view box
def c_invertQTransform(tr):
    """Copied from pyqtgraph functions module
    
        Return a QTransofrm that is the inverse of *tr*
        A pseudo-inverse is returned if tr is not invertible.
        
        Note that this function is preferred over QTransform.inverted() due to
        bugs in that method. Specifically, Qt has floating-point precision issues
        when determining whether a matrix is invertible
    """
    try:
        det = tr.determinant()
        detr = 1.0 / det  ## Let singular matricies raise ZeroDivisionError
        inv = tr.adjoint()
        inv *= detr
        return inv
    except ZeroDivisionError:
        return c_pinv_fallback(tr)


def c_pinv_fallback(tr):
    arr = np.array(
        [
            tr.m11(),
            tr.m12(),
            tr.m13(),
            tr.m21(),
            tr.m22(),
            tr.m23(),
            tr.m31(),
            tr.m32(),
            tr.m33(),
        ]
    )
    arr.shape = (3, 3)
    pinv = np.linalg.pinv(arr)
    return QTransform(*pinv.ravel().tolist())

