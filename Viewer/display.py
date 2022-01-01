''' Module containing functions for generating and updating
    the image display
    
    CREATOR
        William (Jake) Wright - 12/27/2021'''

import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog, QGraphicsEllipseItem, QApplication, QGraphicsRectItem
from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QTransform
import numpy as np

import images
import ROIs


def create_display(parent):
    parent.win = pg.GraphicsLayoutWidget(parent)
    parent.display_image = ImageViewBox(parent)
    #parent.display_image = parent.win.addViewBox(name='Main Image',row=0,col=0)
    parent.win.addItem(parent.display_image,row=0,col=0)
    parent.display_image.setAspectLocked(True)
    parent.lut = pg.HistogramLUTItem()
    parent.LUT = parent.win.addItem(parent.lut)

def Load_File(parent):
    # Load and display image
    filename = QFileDialog.getOpenFileName(parent, 'Open File')[0]
    parent.filename = filename
    # Load the image stack
    ## Generates parent.tif_images
    images.set_display_image(parent,filename)
    # Toggle status of slider and play button
    parent.image_slider.setEnabled(True)
    parent.play_btn.setEnabled(True)
    # Generate display image
    parent.current_image = pg.ImageItem(parent.tif_images[0],border='w')
    parent.display_image.addItem(parent.current_image)
    parent.lut.setImageItem(parent.current_image)
    # Set slider range
    parent.image_slider.setMinimum(0)
    parent.image_slider.setMaximum(len(parent.tif_images)-1)
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
    parent.lut.setLevels(parent.level[0],parent.level[1])

def Play_Video(parent):
    # Play the video of tif images
    if parent.playBtnStatus == 'Off':
        parent.video_timer.timeout.connect(lambda: Play_Update(parent))
        parent.playBtnStatus = 'On'
        parent.video_timer.start(100)
        Play_Update(parent)
    else:
        parent.playBtnStatus = 'Off'
        parent.video_timer.stop()

def Play_Update(parent):
    # Updates display image while playing video
    if parent.idx < len(parent.tif_images)-1:
        parent.idx = parent.idx + 1
    else:
        parent.idx = 0
    parent.level = parent.lut.getLevels()
    parent.image_slider.setValue(parent.idx)
    parent.current_image.setImage(parent.tif_images[parent.idx])
    parent.lut.setLevels(parent.level[0],parent.level[1])


class ImageViewBox(pg.ViewBox):
    '''Custom ViewBox class to display image in.
        Allows mouse click and drag events to be toggled'''
    def __init__(self,parent,*args,**kwargs):
        super(ImageViewBox,self).__init__(*args,**kwargs)
        self.parent = parent

        # Custom Ellipse object to aid in ROI drawing
        self.ImageEllipse = QGraphicsEllipseItem(0,0,1,1)
        self.ImageEllipse.setPen(pg.mkPen((240, 134, 5),width=4))
        self.ImageEllipse.setZValue(1e9)
        self.ImageEllipse.hide()
        self.addItem(self.ImageEllipse,ignoreBounds=True)

    def UpdateEllipse(self,p1,p2):
        rect = QRectF(p1,p2)
        # Ensure ellipse edge is snapped to cursor
        h = rect.height()
        w = rect.width()
        x1 = p1[0] -0.14647*w
        y1 = p1[1] -0.14647*h
        x2 = p2[0] +0.14647*w
        y2 = p2[1] +0.14647*h
        np1 = QPointF(x1,y1)
        np2 = QPointF(x2,y2)
        r = QRectF(np1,np2)
        r = self.childGroup.mapRectFromScene(r)
        self.ImageEllipse.setPos(r.topLeft())
        trScale = QTransform.fromScale(r.width(),r.height())
        self.ImageEllipse.setTransform(trScale)
        self.ImageEllipse.update()
        self.ImageEllipse.show()


    def mouseDragEvent(self,ev, axis=None):
        # Custom mouseDragEvent method
        if self.state['mouseMode'] == pg.ViewBox.RectMode:
            #print('Drag being triggered')
            ev.accept()
            pos = ev.pos()
            dif = (pos-ev.lastPos()) * -1
            mouseEnabled = np.array(self.state['mouseEnabled'],dtype=np.float)
            mask = mouseEnabled.copy()
            if ev.button() & Qt.LeftButton:
                if ev.isFinish():
                    self.ImageEllipse.hide()
                    QApplication.restoreOverrideCursor()
                    self.setMouseMode(pg.ViewBox.PanMode)
                    ROIs.Draw_ROI(self.parent)

                else:
                    self.UpdateEllipse(ev.buttonDownScenePos(ev.button()),ev.scenePos())
        
        else:
            super(ImageViewBox,self).mouseDragEvent(ev)


