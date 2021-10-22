# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import os
import skimage as ski
from skimage import io
from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog as fd
import numpy as np
import matplotlib.pyplot as plt
import cv2




class Activity_Viewer():
    ''' GUI to label neural ROIs and extract fluorescence timecourse from 
        from two-photon imaging videos.
        
        CREATOR
            William (Jake) Wright - 10/20/2021  
            
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
        self.image_pane.grid(row=1,column=1,columnspan=8)
        ### Canvas is an item in the image_pane display
        self.image_canvas = tk.Canvas(self.image_pane,height=500,width=500,
                                       highlightthickness=0) #Change to match image
        self.image_canvas.grid(column=0,row=0,columnspan=4,sticky='nswe')
        
        # Load file button
        self.file_button = tk.Button(self.root,text='Open File',
                                     command=self.Display_Tif,padx=30,pady=5)
        self.file_button.grid(column=0,row=0)
        
        # Image options button
        self.image_options = ['Timecourse', 'Max Project', 'Avg Project']
        self.img_opt_click = tk.StringVar()
        self.img_opt_click.set(self.image_options[0])
        self.img_opt_dropdown = tk.OptionMenu(self.root, self.img_opt_click, *self.image_options,
                                              command=self.Change_Image_Display)
        self.img_opt_dropdown.config(width=15)
        self.img_opt_dropdown.grid(column=1,row=0,stick='w')
        
        
        ## additional states
        self.play_button_on = False ## controls play button state
        
        
        self.filename = None

        
        # Loop GUI
        self.root.mainloop()
    
    
    
    def Load_Tif(self):
        ''' Load the tif stack file and return a list with each image frame'''
        filename = fd.askopenfilename(title='Select File')
        self.filename = filename
        ## Change path to what you would like with initialdir = path
        tif_stack = io.imread(filename,plugin='tifffile')
        # Convert image from int16 to uint8 dtype
        out = np.zeros(np.shape(tif_stack))
        tif_stack = cv2.normalize(tif_stack,out,0,255,cv2.NORM_MINMAX,dtype=cv2.CV_8U)
        self.tif_stack = tif_stack
        tif_list = []
        tif_images = []
        for tif in range(np.shape(tif_stack)[0]):
            i = tif_stack[tif,:,:]
            heat = cv2.applyColorMap(i,cv2.COLORMAP_INFERNO) # can change heatmap color
            h = cv2.cvtColor(heat, cv2.COLOR_RGB2BGR)
            # Matplotlib version (NOT WORKING)
            # cmap = plt.get_cmap('inferno')
            # heat = (cmap(i) * 2**16).astype(np.uint16)[:,:,:3]
            # heat = cv2.cvtColor(heat,cv2.COLOR_RGB2BGR)
            # h = (heat/255).astype(np.uint8)
            # Convert np.array into Tkinter image object
            img = Image.fromarray(h)
            enhancer = ImageEnhance.Brightness(img)
            im = enhancer.enhance(5)
            im = im.resize((500,500),Image.ANTIALIAS) ## Need to make this adaptable to screensize
            img = ImageTk.PhotoImage(im)
            tif_list.append(img)
            tif_images.append(im)
        self.tif_list = tif_list
        self.tif_images = tif_images

    def Display_Tif(self):
        ''' Display the initial tif image in the image pane'''
        if self.filename is None:
            self.Load_Tif()
        else:
            pass
        self.image = self.image_canvas.create_image((self.tif_list[0].width()/2),
                                                    (self.tif_list[0].height()/2),
                                                    anchor='center',image=self.tif_list[0])
        self.slider = tk.Scale(self.image_pane,from_=0,to=len(self.tif_list)-1,
                               orient='horizontal',command=self.Slider_Update,
                               length=(self.tif_list[0].width()*0.75))
        self.slider.grid(column=2,row=1)
        self.forward_button = tk.Button(self.image_pane,text ='>>',
                                        command=self.Forward_Update,
                                        pady=3)
        self.forward_button.grid(column=3,row=1,sticky='swe')
        self.back_button = tk.Button(self.image_pane,text='<<',
                                     command=self.Backward_Update,
                                     pady=3)
        self.back_button.grid(column=1,row=1,sticky='swe')
        self.play_button = tk.Button(self.image_pane, text='>',
                                     command=self.Play_Button_Play,pady=3)
        self.play_button.grid(column=0,row=1,sticky='swe')
        
    def Slider_Update(self,master):
        ''' Function to update displayed image based on the slider'''
        value = self.slider.get()
        self.image_canvas.itemconfig(self.image,image=self.tif_list[value])
    
    def Forward_Update(self):
        ''' Function to update image to the next image by 1'''
        if self.slider.get() == (len(self.tif_list)-1):
            pass
        else:
            newvalue = self.slider.get()+1
            self.image_canvas.itemconfig(self.image,image=self.tif_list[newvalue])
            self.slider.set(newvalue)
    
    def Backward_Update(self):
        ''' Function to update image to the previous image by 1 '''
        if self.slider.get() == 0:
            pass
        else:
            newvalue = self.slider.get()-1
            self.image_canvas.itemconfig(self.image,image=self.tif_list[newvalue])
            self.slider.set(newvalue)
        
    def Play_Update(self,v=None):
        ''' Function to play through the images'''

        if self.play_button_on is True:
            self.play_button['text'] = '||'
            if v is None:
                v = self.slider.get()
            else:
                v = v
                if v < (len(self.tif_list)):
                    self.image_canvas.itemconfig(self.image,image=self.tif_list[v])
                    self.slider.set(v)
                    
                else:
                    v = 0
                    self.image_canvas.itemconfig(self.image,image=self.tif_list[v])
                    self.slider.set(0)
        else:
            self.play_button['text'] = '>'
            return
        self.root.after(100,self.Play_Update,v+1)
    
    def Play_Button_Play(self):
        ''' Function to control Play Button State'''
        if self.play_button_on is False:
            self.play_button_on = True
        else:
            self.play_button_on = False
        self.Play_Update()
    
    def Change_Image_Display(self,master):
        ''' Function to change the display of the image'''
        option = self.img_opt_click.get()
        if option == 'Timecourse':
            self.Display_Tif()
        elif option == 'Max Project':
            self.Max_Project()
        elif option == 'Avg Project':
            self.Avg_Project()
        else:
            return
    
    def Max_Project(self):
        ''' Function to generated a max projection of the image'''
        tif_stack = self.tif_stack
        max_array = np.amax(tif_stack,axis=0)
        heat = cv2.applyColorMap(max_array,cv2.COLORMAP_INFERNO) # can change heatmap color
        h_max = cv2.cvtColor(heat, cv2.COLOR_RGB2BGR)
        ima = Image.fromarray(h_max)
        enhancer = ImageEnhance.Brightness(ima)
        im = enhancer.enhance(5)
        im = im.resize((500,500),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im)
        self.max_project = img
        self.slider['state'] = 'disabled'
        self.play_button['state'] = 'disabled'
        self.forward_button['state'] = 'disabled'
        self.back_button['state'] = 'disabled'
        self.image_canvas.itemconfig(self.image,image=self.max_project)

    
    def Avg_Project(self):
        ''' Function to generate an avg projection of the image'''
        tif_stack = self.tif_stack
        avg_array = np.mean(tif_stack,axis=0).astype(np.uint8)
        heat = cv2.applyColorMap(avg_array,cv2.COLORMAP_INFERNO) # can change heatmap color
        h_avg = cv2.cvtColor(heat, cv2.COLOR_RGB2BGR)
        ima = Image.fromarray(h_avg)
        enhancer = ImageEnhance.Brightness(ima)
        im = enhancer.enhance(5)
        im = im.resize((500,500),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(im)
        self.avg_project = img
        self.slider['state'] = 'disabled'
        self.play_button['state'] = 'disabled'
        self.forward_button['state'] = 'disabled'
        self.back_button['state'] = 'disabled'
        self.image_canvas.itemconfig(self.image,image=self.avg_project)
        


if __name__ == '__main__':
    Activity_Viewer(tk.Tk())