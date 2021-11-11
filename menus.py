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
    