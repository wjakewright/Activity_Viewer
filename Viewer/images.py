
''' Module containing functions to handle display of the 
    images for Activity_Viewer GUI'''

import cv2
import numpy as np
from skimage import io as sio

def set_display_image(parent,filename):
    # Loads the image file and performs initial processing
    # Performs initial processing

    tif_stack = sio.imread(filename,plugin='tifffile')
    # Normalize to unit dtype
    out = np.zeros(np.shape(tif_stack))
    tif_stack = cv2.normalize(tif_stack,out,0,255,cv2.NORM_MINMAX,dtype=cv2.CV_8U)
    # Process each image in the stack
    tif_images = []
    for tif in range(np.shape(tif_stack)[0]):
        i = tif_stack[tif,:,:]
        # set color map to image
        if parent.color_map == 'Inferno':
            heat = cv2.applyColorMap(i,cv2.COLORMAP_INFERNO)
        elif parent.color_map == 'Cividis':
            heat = cv2.applyColorMap(i,cv2.COLORMAP_CIVIDIS)
        elif parent.color_map == 'Plasma':
            heat = cv2.applyColorMap(i,cv2.COLORMAP_PLASMA)
        elif parent.color_map == 'Hot':
            heat = cv2.applyColorMap(i,cv2.COLORMAP_HOT)
        else:
            pass

        # Threshold Image
        _, img = cv2.threshold(heat,parent.img_threshold,255,cv2.THRESH_TOZERO)

        # Adjust brightness
        img = gamma_correction(parent.gamma,img)

        # Adjust image size
        img = cv2.resize(img,parent.image_size)

        # Ensure dtype is uint8
        img = (img).astype(np.uint8)
        tif_images.append(img)

    parent.tif_images = tif_images


def gamma_correction(gamma,image):
    # Gamma correction method
    inv_gamma =  1/gamma
    table = [((i/255) ** inv_gamma) * 255 for i in range(256)]
    table = np.array(table,np.uint8)

    return cv2.LUT(image,table)