""" Module containing functions to handle display of the 
    images for Activity_Viewer GUI
    
    CREATOR
        William (Jake) Wright - 12/18/2021"""

import cv2
import numpy as np
from skimage import io as sio


def set_display_image(parent, filename):
    # Loads the image file and performs initial processing
    # Performs initial processing
    if parent.tif_stack is None:
        tif_stack = sio.imread(filename, plugin="tifffile")
        # Normalize to unit dtype
        out = np.zeros(np.shape(tif_stack))
        tif_stack = cv2.normalize(
            tif_stack, out, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )
        parent.tif_stack = tif_stack
    else:
        tif_stack = parent.tif_stack
    # Process each image in the stack
    tif_images = []
    for tif in range(np.shape(tif_stack)[0]):
        i = tif_stack[tif, :, :]
        img = process_images(parent, i)
        tif_images.append(img)

    parent.tif_images = tif_images


def process_images(parent, image):
    # Function to proecess individual images
    i = image
    # set color map to image
    if parent.color_map == "Inferno":
        heat = cv2.applyColorMap(i, cv2.COLORMAP_INFERNO)
    elif parent.color_map == "Cividis":
        heat = cv2.applyColorMap(i, cv2.COLORMAP_CIVIDIS)
    elif parent.color_map == "Plasma":
        heat = cv2.applyColorMap(i, cv2.COLORMAP_PLASMA)
    elif parent.color_map == "Hot":
        heat = cv2.applyColorMap(i, cv2.COLORMAP_HOT)
    else:
        pass
    if parent.color_map == "Gray":
        heat = i
    else:
        heat = cv2.cvtColor(heat, cv2.COLOR_BGR2RGB)

    # Threshold Image
    _, img = cv2.threshold(heat, parent.img_threshold, 255, cv2.THRESH_TOZERO)

    # Adjust brightness
    img = gamma_correction(parent.gamma, img)

    # Adjust image size
    img = cv2.resize(img, parent.image_size)

    # Ensure dtype is uint8
    img = (img).astype(np.uint8)

    return img


def gamma_correction(gamma, image):
    # Gamma correction method
    inv_gamma = 1 / gamma
    table = [((i / 255) ** inv_gamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(image, table)


def set_cmap(parent, c_map):
    # Generic cmap function
    parent.color_map = c_map
    if parent.image_status == "video":
        set_display_image(parent, parent.filename)
        parent.current_image.setImage(parent.tif_images[parent.idx])
    elif parent.image_status == "max":
        get_max_project(parent)
    elif parent.image_status == "avg":
        get_avg_project(parent)
    # parent.Update_Image()


def get_projection(parent, type):
    # Get projection of the image
    if type == "max":
        tif_proj = np.amax(parent.tif_stack, axis=0)
        tif_projection = process_images(parent, tif_proj)

    elif type == "avg":
        tif_proj = np.mean(parent.tif_stack, axis=0).astype(np.uint8)
        tif_projection = process_images(parent, tif_proj)

    return tif_projection


def get_max_project(parent):
    t = "max"
    max_tif = get_projection(parent, t)
    parent.current_image.setImage(max_tif)
    parent.image_slider.setEnabled(False)
    parent.play_btn.setEnabled(False)
    parent.image_status = "max"


def get_avg_project(parent):
    t = "avg"
    avg_tif = get_projection(parent, t)
    parent.current_image.setImage(avg_tif)
    parent.image_slider.setEnabled(False)
    parent.play_btn.setEnabled(False)
    parent.image_status = "avg"


def display_video(parent):
    parent.image_slider.setEnabled(True)
    parent.play_btn.setEnabled(True)
    parent.image_slider.setValue(0)
    parent.current_image.setImage(parent.tif_images[0])
    parent.image_status = "video"
