# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import skimage as ski
from skimage import io
from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog as fd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.widgets as mwidget
from matplotlib.figure import Figure
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
        self.root.config(bg='#161616')

        
        
        # Frame for image display
        self.image_pane = tk.Frame(self.root,bg='#161616')
        self.image_pane.grid(row=1,column=1,columnspan=2)
        ### Canvas is an item in the image_pane display
        self.fig = Figure()
        self.image_frame = tk.Frame(self.image_pane,bg='#161616')
        self.image_frame.grid(column=0,row=0,columnspan=4,sticky='nswe')
        self.image_canvas = tkagg.FigureCanvasTkAgg(self.fig,master=self.image_frame)
        self.image_canvas.get_tk_widget().config(width=500,height=500)
        self.image_canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH)
        self.image_canvas.get_tk_widget().bind('<Motion>',self.position)
        ## Adding frame to put scale bar and buttons in
        self.slider_frame = tk.Frame(self.image_pane,height=50,bg='#161616')
        self.slider_frame.grid(column=0,row=1,sticky='nswe')
        ## Adding zoom functionality to the canvas
        tkagg.NavigationToolbar2Tk(self.image_canvas,self.image_frame)
        
        # Load file button
        self.file_button = tk.Button(self.root,text='Open File', highlightbackground='#161616',
                                     fg='white',relief='flat',
                                     command=self.Display_Tif,padx=30,pady=5)
        self.file_button.grid(column=0,row=0,padx=3)
        
        # Image options button
        self.image_options = ['Timecourse', 'Max Project', 'Avg Project']
        self.img_opt_dropdown = ttk.Combobox(self.root,value=self.image_options)
        self.img_opt_dropdown.current(0)
        self.img_opt_dropdown.bind('<<ComboboxSelected>>',self.Change_Image_Display)
        self.img_opt_dropdown.grid(column=1,row=0,sticky='w')
        self.img_opt_dropdown.config(width=15)
        

        # Draw ROI panel
        self.ROI_frame = tk.Frame(self.root,bg='#161616',highlightbackground='#5A5A5A',highlightthickness=2)
        self.ROI_frame.grid(column=0,row=1,sticky='nswe',padx=3,pady=3)

    
        ## additional states
        self.play_button_on = False ## controls play button state
        
        
        self.filename = None
        self.image = None

        # Loop GUI
        self.root.mainloop()
    
    
    def position(self,event):
        ''' Function to display the x y position of the mouse over the canvas'''
        self.x, self.y = event.x, event.y
        self.myxy = tk.Label(self.image_frame, text = "Position: " + str(self.x) + ", " + str(self.y),
                             bg='black',fg='white',padx=5)
        self.myxy.place(x=0,y=0)
        
        
    def plt_fig(self,value,image=None):
        ''' Function to display the image on the Canvas'''
        self.fig.clear()
        self.axes = self.fig.add_axes([0,0,1,1])
        self.fig.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=None,hspace=None)
        if image is None:
            self.axes.imshow(self.tif_list[value])
            self.axes.axis('off') 
            self.image_canvas.draw()
        else:
            self.axes.imshow(image)
            self.axes.axis('off')
            self.image_canvas.draw()

        
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
            # pseudocolor with heatmap
            heat = cv2.applyColorMap(i,cv2.COLORMAP_INFERNO) # can change heatmap color
            h = cv2.cvtColor(heat, cv2.COLOR_RGB2BGR)
            # Matplotlib version (NOT WORKING)
            # cmap = plt.get_cmap('inferno')
            # heat = (cmap(i) * 2**16).astype(np.uint16)[:,:,:3]
            # h = (heat/255).astype(np.uint8)
            # Convert np.array into Tkinter image object
            img = Image.fromarray(h)
            enhancer = ImageEnhance.Brightness(img)
            im = enhancer.enhance(5)
            im = im.resize((500,500),Image.ANTIALIAS)## Need to make this adaptable to screensize
            img = np.array(im)
            tif_list.append(img)
            tif_images.append(im)
        self.tif_list = tif_list
        self.tif_images = tif_images


    def Display_Tif(self):
        ''' Display the initial tif image in the image pane'''
        # Load images if not yet loaded
        if self.filename is None:
            self.Load_Tif()
        else:
            pass
        # create the image up on the canvas
        self.plt_fig(0)
        
        self.slider = tk.Scale(self.image_pane,from_=0,to=len(self.tif_list)-1,
                               orient='horizontal',command=self.Slider_Update,
                               length=300)
        self.slider.grid(column=2,row=1)
        self.forward_button = tk.Button(self.image_pane,text ='>>',
                                        command=self.Forward_Update,pady=3)
        self.forward_button.grid(column=3,row=1,sticky='swe')
        self.back_button = tk.Button(self.image_pane,text='<<',
                                     command=self.Backward_Update,pady=3)
        self.back_button.grid(column=1,row=1,sticky='swe')
        self.play_button = tk.Button(self.image_pane, text='>',
                                     command=self.Play_Button_Play,pady=3)
        self.play_button.grid(column=0,row=1,sticky='swe')
        
        
    def Slider_Update(self,master):
        ''' Function to update displayed image based on the slider'''
        value = self.slider.get()
        self.plt_fig(value)
    
    
    def Forward_Update(self):
        ''' Function to update image to the next image by 1'''
        if self.slider.get() == (len(self.tif_list)-1):
            pass
        else:
            newvalue = self.slider.get()+1
            self.plt_fig(newvalue)
            self.slider.set(newvalue)
    
    
    def Backward_Update(self):
        ''' Function to update image to the previous image by 1 '''
        if self.slider.get() == 0:
            pass
        else:
            newvalue = self.slider.get()-1
            self.plt_fig(newvalue)
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
                    self.plt_fig(v)
                    self.slider.set(v)
                    
                else:
                    v = 0
                    self.plt_fig(v)
                    self.slider.set(0)
        else:
            self.play_button['text'] = '>'
            return
        self.root.after(50,self.Play_Update,v+1)
    
    
    def Play_Button_Play(self):
        ''' Function to control Play Button State'''
        if self.play_button_on is False:
            self.play_button_on = True
        else:
            self.play_button_on = False
        self.Play_Update()
    
    
    def Change_Image_Display(self,master):
        ''' Function to change the display of the image'''
        option = self.img_opt_dropdown.get()
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
        img = np.array(im)
        self.max_project = img
        self.slider['state'] = 'disabled'
        self.play_button['state'] = 'disabled'
        self.forward_button['state'] = 'disabled'
        self.back_button['state'] = 'disabled'
        self.plt_fig(value=0,image=img)

    
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
        img = np.array(im)
        self.avg_project = img
        self.slider['state'] = 'disabled'
        self.play_button['state'] = 'disabled'
        self.forward_button['state'] = 'disabled'
        self.back_button['state'] = 'disabled'
        self.plt_fig(value=0,image=img)
        


if __name__ == '__main__':
    Activity_Viewer(tk.Tk())