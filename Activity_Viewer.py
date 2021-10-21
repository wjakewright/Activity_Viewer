# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import os
import skimage as ski
from skimage import io
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import numpy as np
import matplotlib.pyplot as plt
import cv2




class Activity_Viewer():
    ''' GUI to label neural ROIs and extract fluorescence timecourse from 
        from two-photon imaging videos.
        
        CREATOR
            Williame (Jake) Wright - 10/20/2021  
            
    '''
    
    def __init__(self,root):
        ''' Creating the GUI'''
        
        #Initialize the GUI object
        self.root = root
        self.root.title('Activity Viewer')
        #Specify the size of GUI relative to monitor screen size
        sc_w = int(root.winfo_screenwidth() *0.8)
        sc_h = int(root.winfo_screenheight() *0.8)
        c_x = int(root.winfo_screenwidth()/2 - sc_w/2)
        c_y = int(root.winfo_screenheight()/2 - sc_h/2)
        self.root.geometry(f'{sc_w}x{sc_h}+{c_x}+{c_y}')
        
        # Frame for image display
        self.image_pane = tk.Frame(self.root)
        self.image_pane.grid(row=1,column=1)
        
        # Load file button
        self.file_button = tk.Button(self.root,text='Open File',
                                     command=self.Display_Tif)
        self.file_button.grid(column=0,row=0)
        
        ## additional states
        self.play_button_on = False ## controls play button state

        
        # Loop GUI
        self.root.mainloop()
    
    
    
    def Load_Tif(self):
        ''' Load the tif stack file and return a list with each image frame'''
        filename = fd.askopenfilename(title='Select File')
        ## Change path to what you would like with initialdir = path
        tif_stack = io.imread(filename,plugin='tifffile')
        # Convert image from int16 to uint8 dtype
        out = np.zeros(np.shape(tif_stack))
        self.tif_stack = tif_stack
        tif_stack = cv2.normalize(tif_stack,out,0,255,cv2.NORM_MINMAX).astype(np.uint8)
        tif_list = []
        for tif in range(np.shape(tif_stack)[0]):
            i = tif_stack[tif,:,:]
            heat = cv2.applyColorMap(i,cv2.COLORMAP_HOT) # can change heatmap color
            h = cv2.cvtColor(heat, cv2.COLOR_RGB2BGR)
            # Matplotlib version (NOT WORKING)
            # cmap = plt.get_cmap('inferno')
            # heat = (cmap(i) * 2**16).astype(np.uint16)[:,:,:3]
            # heat = cv2.cvtColor(heat,cv2.COLOR_RGB2BGR)
            # h = (heat/255).astype(np.uint8)
            # Convert np.array into Tkinter image object
            im = Image.fromarray(h)
            im = im.resize((700,700),Image.ANTIALIAS) ## Need to make this adaptable to screensize
            img = ImageTk.PhotoImage(im)
            tif_list.append(img)
        self.tif_list = tif_list

    def Display_Tif(self):
        ''' Display the initial tif image in the image pane'''
        self.Load_Tif()
        self.image = tk.Label(self.image_pane,image=self.tif_list[0])
        self.image.grid(column=0,row=0,columnspan=4,sticky='nswe')
        self.slider = tk.Scale(self.image_pane,from_=0,to=len(self.tif_list)-1,
                               orient='horizontal',command=self.Slider_Update,
                               length=(self.tif_list[0].width()*0.85))
        self.slider.grid(column=2,row=1)
        # Additing buttons to play or go through frames individually
        self.forward_button = tk.Button(self.image_pane,text ='>>',
                                        command=self.Forward_Update)
        self.forward_button.grid(column=3,row=1,sticky='swe')
        self.back_button = tk.Button(self.image_pane,text='<<',
                                     command=self.Backward_Update)
        self.back_button.grid(column=1,row=1,sticky='swe')
        self.play_button = tk.Button(self.image_pane, text='>',
                                     command=self.Play_Button_Play)
        self.play_button.grid(column=0,row=1,sticky='swe')
        
    def Slider_Update(self,master):
        ''' Function to update displayed image based on the slider'''
        value = self.slider.get()
        self.image.configure(image=self.tif_list[value])
    
    def Forward_Update(self):
        ''' Function to update image to the next image by 1'''
        if self.slider.get() == (len(self.tif_list)-1):
            pass
        else:
            newvalue = self.slider.get()+1
            self.image.configure(image=self.tif_list[newvalue])
            self.slider.set(newvalue)
    
    def Backward_Update(self):
        ''' Function to update image to the previous image by 1 '''
        if self.slider.get() == 0:
            pass
        else:
            newvalue = self.slider.get()-1
            self.image.configure(image=self.tif_list[newvalue])
            self.slider.set(newvalue)
        
    def Play_Update(self,start_v=None):
        ''' Function to play through the images'''
        #st = next(self.play_button_state)
        #if st == 0:
        if self.play_button_on is True:
            if start_v is None:
                start_v = self.slider.get()
            else:
                start_v = start_v
                if start_v < (len(self.tif_list)):
                    self.image['image'] = self.tif_list[start_v]
                    self.slider.set(start_v)
                    
                else:
                    self.image['image'] = self.tif_list[0]
                    self.slider.set(0)
        else:
            return
        self.root.after(100,self.Play_Update,start_v+1)
    
    def Play_Button_Play(self):
        ''' Function to control Play Button State'''
        if self.play_button_on is False:
            self.play_button_on = True
        else:
            self.play_button_on = False
        self.Play_Update()
        


if __name__ == '__main__':
    Activity_Viewer(tk.Tk())