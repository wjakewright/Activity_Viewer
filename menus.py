#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Module containing different menus for Activity Viewer GUI
    
    CREATOR
        William (Jake) Wright - 11/11/2021'''

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QMenu
        
def mainMenu(parent):
    ''' Main Menu bar for the GUI'''
    main_menu = parent.menuBar()
    
    # Load Image Files
    open_file = QAction('&Open File', parent)
    open_file.setShortcut('Ctrl+O')
    open_file.triggered.connect(lambda: print('file opened'))
    
    
    # Main Main Menu Bar
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
    file_menu.addAction(open_file)
    
    