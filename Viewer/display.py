''' Module containing functions for generating and updating
    the image display
    
    CREATOR
        William (Jake) Wright - 12/27/2021'''

import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog

import images


def create_display(parent):
    parent.win = pg.GraphicsLayoutWidget(parent)
    parent.display_image = parent.win.addPlot(title='Main Image',row=0,col=0)
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

