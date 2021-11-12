#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Module containing different menus for Activity Viewer GUI
    
    CREATOR
        William (Jake) Wright - 11/11/2021'''

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QMenu, QFileDialog
        
def fileMenu(parent):
    ''' Main Menu bar for the GUI'''
    main_menu = parent.menuBar()
    
    # --------MAIN MENU BAR--------
    
    # Load Image Files
    parent.open_image = QAction('&Open Image', parent)
    parent.open_image.setShortcut('Ctrl+O')
    parent.open_image.triggered.connect(lambda: parent.Load_file())
    
    # Load ROIs
    parent.load_ROIs = QAction('&Load ROIs', parent)
    parent.load_ROIs.setShortcut('Ctrl+L')
    parent.load_ROIs.triggered.connect(lambda: print('add functionality'))
    
    # Save ROIs 
    parent.save_ROIs = QAction('&Save ROIs', parent)
    parent.save_ROIs.setShortcut('Ctrl+S')
    parent.save_ROIs.triggered.connect(lambda: print('add functionality'))
    
    
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
    
    

    
    
    
    
    