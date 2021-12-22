#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Module containing different menus for Activity Viewer GUI
    
    CREATOR
        William (Jake) Wright - 11/11/2021'''

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QMenu, QFileDialog
from cv2 import Param_UNSIGNED_INT
import images
        
def fileMenu(parent):
    ''' Main Menu bar for the GUI'''
    main_menu = parent.menuBar()
    
    # --------MAIN MENU BAR--------
    
    # Load Image Files
    parent.open_image = QAction('&Open Image', parent)
    parent.open_image.setShortcut('Ctrl+O')
    parent.open_image.triggered.connect(lambda: parent.Display_Image())
    
    # Load ROIs
    parent.load_ROIs = QAction('&Load ROIs', parent)
    parent.load_ROIs.setShortcut('Ctrl+L')
    parent.load_ROIs.triggered.connect(lambda: print('add functionality'))
    
    # Save ROIs 
    parent.save_ROIs = QAction('&Save ROIs', parent)
    parent.save_ROIs.setShortcut('Ctrl+S')
    parent.save_ROIs.triggered.connect(lambda: print('add functionality'))

    # Start new session
    parent.new_session = QAction('&New Session', parent)
    parent.new_session.setShortcut('Ctrl+N')
    parent.new_session.triggered.connect(lambda: print('add functionality'))

    # Exit Viewer
    parent.exit_viewer = QAction('&Exit', parent)
    parent.exit_viewer.setShortcut('Ctrl+ESC')
    parent.exit_viewer.triggered.connect(lambda: parent.close())
    
    
    # Make Main Menu Bar
    main_menu = parent.menuBar()
    main_menu.setStyleSheet('''QMenuBar {
                                        background-color: #132743;
                                        color:white;}
                                QMenuBar::item {
                                        background-color: #132743;
                                        color:white;}
                                QMenuBar::item:selected {
                                        background-color: #02449B;}
                                QMenu {
                                        background-color: #132743;
                                        color:white;}
                                QMenu::item {
                                        background-color: #132743;
                                        color:white;}
                                QMenu::item:selected {
                                        background-color: #02449B;
                                        color:white;}''')
    main_menu.setNativeMenuBar(False)
    file_menu = main_menu.addMenu('&File')
    file_menu.addAction(parent.open_image)
    file_menu.addAction(parent.load_ROIs)
    file_menu.addAction(parent.save_ROIs)
    file_menu.addAction(parent.new_session)
    file_menu.addAction(parent.exit_viewer)
    
def imageMenu(parent):
    main_menu = parent.menuBar()
    #------Image Settings Menu-----
    
    main_menu = parent.menuBar()
    image_menu = main_menu.addMenu('&Image')
    
    # Select Colormap
    parent.cmap = image_menu.addMenu('&Color Map')
    ## Colormap Options
    parent.inferno = QAction('&Inferno', parent)
    parent.inferno.triggered.connect(lambda: images.set_cmap(parent,'Inferno'))
    parent.cividis = QAction('&Cividis', parent)
    parent.cividis.triggered.connect(lambda: images.set_cmap(parent,'Cividis'))
    parent.plasma = QAction('&Plasma', parent)
    parent.plasma.triggered.connect(lambda: images.set_cmap(parent,'Plasma'))
    parent.hot = QAction('&Hot', parent)
    parent.hot.triggered.connect(lambda: images.set_cmap(parent,'Hot'))
    parent.gray = QAction('&Gray',parent)
    parent.gray.triggered.connect(lambda: print('add functionality'))
    
    parent.cmap.addAction(parent.gray)
    parent.cmap.addAction(parent.hot)
    parent.cmap.addAction(parent.inferno)
    parent.cmap.addAction(parent.plasma)
    parent.cmap.addAction(parent.cividis)

    # Select Display Options
    parent.disp_options = image_menu.addMenu('&Display Options')
    ## Display options
    parent.img_video = QAction('&Video', parent)
    parent.img_video.triggered.connect(lambda: images.display_video(parent))
    parent.img_max_z = QAction('&Max Project', parent)
    parent.img_max_z.triggered.connect(lambda: images.get_max_project(parent))
    parent.img_avg_z = QAction('&Avg Project', parent)
    parent.img_avg_z.triggered.connect(lambda: images.get_avg_project(parent))
    
    parent.disp_options.addAction(parent.img_video)
    parent.disp_options.addAction(parent.img_max_z)
    parent.disp_options.addAction(parent.img_avg_z)


    
    
    
    
    