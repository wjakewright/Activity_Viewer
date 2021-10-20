# -*- coding: utf-8 -*-
import tkinter as tk
import skimage as ski
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
        
        # Loop GUI
        self.root.mainloop()
    
    
    
    def Load_Tif(self):
        ''' Load the tif stack file and return a list with each image frame'''
        filename = fd.askopenfilename(title='Select File',initialdir=r'C:\Users\Jake\Desktop\python_code\Activity_Viewer')
        tif_stack = ski.io.imread(filename,plugin='tifffile')
        self.tif_stack = tif_stack
        tif_list = []
        for tif in range(np.shape(tif_stack)[0]):
            i = tif_stack[tif,:,:]
            # Convert image from type int16 to uint8
            out = np.zeros(np.shape(i))
            i = cv2.normalize(i,out,0,255,cv2.NORM_MINMAX).astype(np.uint8)
            # Convert to Heatmap for better visualization
            # cv2 implementation
            heat = cv2.applyColorMap(i,cv2.COLORMAP_JET) # can change heatmap color
            heat = cv2.cvtColor(heat, cv2.COLOR_RGB2BGR)
            #Matplotlib version (NOT WORKING)
            # cmap = plt.get_cmap('inferno')
            # heat = (cmap(i) * 2**16).astype(np.uint16)[:,:,:3]
            # heat = cv2.cvtColor(heat,cv2.COLOR_RGB2BGR)
            # h = (heat/255).astype(np.uint8)
            # Convert np.array into Tkinter image object
            im = Image.fromarray(heat)
            im = im.resize((700,700),Image.ANTIALIAS) ## Need to make this adaptable to screensize
            img = ImageTk.PhotoImage(im)
            tif_list.append(img)
        self.tif_list = tif_list

    def Display_Tif(self):
        ''' Display the initial tif image in the image pane'''
        self.Load_Tif()
        self.image = tk.Label(self.image_pane,image=self.tif_list[0])
        self.image.grid(column=0,row=0,sticky='nswe')
        self.slider = tk.Scale(self.image_pane,from_=0,to=len(self.tif_list),
                               orient='horizontal',command=self.Update_Image)
        self.slider.grid(column=0,row=1,sticky='nswe')
        
    def Update_Image(self):
        ''' Function to update displayed image based on the slider'''
        
        
    
        
        
        
        
        


if __name__ == '__main__':
    Activity_Viewer(tk.Tk())