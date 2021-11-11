#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Module containing different menus for Activity Viewer GUI
    
    CREATOR
        William (Jake) Wright - 11/11/2021'''

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QMenu, QFileDialog
        
def mainMenu(parent):
    ''' Main Menu bar for the GUI'''
    main_menu = parent.menuBar()
    
    # --------MAIN MENU BAR--------
    
    # Load Image Files
    parent.open_file = QAction('&Open File', parent)
    parent.open_file.setShortcut('Ctrl+O')
    parent.open_file.triggered.connect(lambda: parent.Load_file())
    
    
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
    file_menu.addAction(parent.open_file)
    

    
    
    
    
    