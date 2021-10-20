# -*- coding: utf-8 -*-
import tkinter as tk
import skimage as ski
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import numpy as np



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
        filename = fd.askopenfilename(title='Select File',initialdir=r'C:\Users\Jake\Desktop\python_code\Activity_Viewer')
        tif_stack = ski.io.imread(filename)
        self.tif_stack = tif_stack
        tif_list = []
        for tif in range(np.shape(tif_stack)[0]):
            im = Image.fromarray(tif_stack[tif,:,:])
            img = ImageTk.PhotoImage(im)
            tif_list.append(img)
        self.tif_list = tif_list
    
    def Display_Tif(self):
        self.Load_Tif()
        self.image = tk.Label(self.image_pane,image=self.tif_list[0])
        self.image.pack()
        
        
        
        


if __name__ == '__main__':
    Activity_Viewer(tk.Tk())