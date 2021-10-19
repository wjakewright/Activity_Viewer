#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as Tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image


def Activity_Viewer():
    ''' GUI to label neural ROIs and extract fluorescence timecourse from 
        from two-photon imaging videos.
        
        CREATOR
            Williame (Jake) Wright - 10/18/2021  
            
    '''
    
    root = Tk.Tk()
    root.title('Activity Viewer')
    root.geometry('500x500')

    
    
    def select_image_files():
        #filetypes = (('tif files','*.tif'))
        filename = fd.askopenfilename(title='Select File',initialdir='/Users/williamwright/Desktop/')
        #showinfo(title='Selected File',message=filename)
        im = ImageTk.PhotoImage(Image.open(filename))
        ## Weird Tkinter behavior. Must keep a reference of the image object in the widget
        ## for Tkinter to use for further reference. Otherwise it destroys it.
        panel = Tk.Label(root,image=im)
        panel.image = im
        panel.pack()
        
    
    
    open_button = ttk.Button(root,text='Select a File',command=select_image_files)

    open_button.pack(expand=True)
    
    
    
    
    
    
    
    
    
    root.mainloop()
    
if __name__ == '__main__':
    Activity_Viewer()
    