#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as Tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
import skimage as ski
import numpy as np


def Activity_Viewer():
    ''' GUI to label neural ROIs and extract fluorescence timecourse from 
        from two-photon imaging videos.
        
        CREATOR
            Williame (Jake) Wright - 10/18/2021  
            
    '''
    
    root = Tk.Tk()
    # Set window location and size relative to computer
    # screen size
    sc_w = int(root.winfo_screenwidth() *0.8)
    sc_h = int(root.winfo_screenheight() *0.8)
    c_x = int(root.winfo_screenwidth()/2 - sc_w/2)
    c_y = int(root.winfo_screenheight()/2 - sc_h/2)
    #win_size = str(sc_w*.9) +'x' + str(sc_h*.9)
    root.title('Activity Viewer')
    root.geometry(f'{sc_w}x{sc_h}+{c_x}+{c_y}') #wxh
    
    # Set canvas for image display
    image_window = Tk.Frame(root)
    image_window.grid(row=1,column=1)
            
    
    def Update_Image(event):
        return
    
    def display_tif(filename):
        tif_stack = ski.io.imread(filename)
        tif_list = []
        for tif in range(np.shape(tif_stack)[0]):
            im = Image.fromarray(tif_stack[tif,:,:])
            img = ImageTk.PhotoImage(im)
            tif_list.append(img)
        slider = Tk.Scale(image_window,from_=0,to=len(tif_list),
                          orient='horizontal',command=Update_Image)
        return tif_list
        
    
    def select_image_files():
        #filetypes = (('tif files','*.tif'))
        filename = fd.askopenfilename(title='Select File',initialdir=r'C:\Users\Jake\Desktop\python_code\Activity_Viewer')
        tif_list = display_tif(filename)
        ## Weird Tkinter behavior. Must keep a reference of the image object in the widget
        ## for Tkinter to use for further reference. Otherwise it destroys it.
        panel = Tk.Label(image_window,image=tif_list[55])
        panel.image = tif_list[55]
        panel.pack()
        
    
    
    open_button = ttk.Button(root,text='Select a File',command=select_image_files)

    open_button.grid(column=0,row=0)
    

    
    root.mainloop()
    
if __name__ == '__main__':
    Activity_Viewer()
    