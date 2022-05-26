"""Module for creating window to visualize the final outputs after processing"""

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDesktopWidget,
    QDialog,
    QGridLayout,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import styles


class Output_Window(QDialog):
    """Custom window to display the outputs after processing"""

    def __init__(self, parent):
        super(Output_Window, self).__init__(parent=parent)
        self.parent = parent

        # Set up window properties
        pg.setConfigOptions(imageAxisOrder="row-major")
        screen_size = QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.8)
        win_w = int(screen_size.width() * 0.8)
        self.setGeometry(70, 70, win_w, win_h)
        self.setWindowTitle("Examine Outputs")

        self.initWindow()

    def initWindow(self):
        """Putting everything in the window"""

        self.data_to_display = []
        self.plot_items = []
        self.plot_widgets = []

        # Set up grid layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Make data display control frame
        display_control_window(self.parent, self)

        # Make roi list display
        roi_list_display(self.parent, self)

        # Make the side panel display
        self.side_panel = QWidget()
        side_panel_layout = QVBoxLayout()
        self.side_panel.setLayout(side_panel_layout)
        self.side_panel.setFixedWidth(130)
        side_panel_layout.addWidget(self.control_widget)
        side_panel_layout.addWidget(self.roi_list_display)
        side_panel_layout.addStretch(1)

        # Make the plot area
        self.plot_window = QWidget()
        self.plot_window_layout = QGridLayout()
        self.plot_window.setLayout(self.plot_window_layout)

        # Add items to the grid layout
        self.grid_layout.addWidget(self.side_panel, 0, 0)
        self.grid_layout.addWidget(self.plot_window, 0, 1)


def set_display_data(win, data_type):
    """Function to update what data to display"""
    if data_type not in win.data_to_display:
        win.data_to_display.append(data_type)
    else:
        win.data_to_display.remove(data_type)

    update_plot_area(win)


def update_plot_area(win):
    """Function to update the plotting area in the window"""
    # clearing existing plot items to reset everything
    if win.plot_widgets:
        for i in win.plot_widgets:
            win.plot_window_layout.removeWidget(i)
            i.hide()
    del win.plot_widgets[:]
    del win.plot_items[:]

    # Make all the plot items and widgets
    for i, item in enumerate(win.data_to_display):
        plot = pg.PlotItem()
        plot.setTitle(item)
        plot.setMouseEnabled(y=False)
        plot.addLegend()
        plot_widget = pg.PlotWidget(win, plotItem=plot)
        win.plot_items.append(plot)
        win.plot_widgets.append(plot_widget)
        row = i - 2 if i - 2 >= 0 else i
        column = i // 2
        win.plot_window_layout.addWidget(win.plot_widgets[i], row, column)

    # Link all the x axis for simultaneous zooming
    if len(win.plot_widgets) > 1:
        for i in win.plot_widgets[1:]:
            i.setXLink(win.plot_widgets[0])


def display_control_window(parent, win):
    """Makes the display control window that allows you to determine 
        what data you wish to visualize"""
    control_layout = QVBoxLayout()
    win.control_widget = QGroupBox(win, title="Display Data")
    win.control_widget.setStyleSheet(styles.roiFrameStyle())
    win.control_widget.setFont(styles.roi_btn_font())
    win.control_widget.setLayout(control_layout)
    win.control_widget.setFixedWidth(120)

    #### ADD BUTTONS ####

    # fluorescence button
    win.fluorescence_btn = QPushButton("Fluorescence")
    win.fluorescence_btn.setStyleSheet(styles.roiBtnStyle())
    win.fluorescence_btn.setFont(styles.roi_btn_font())
    win.fluorescence_btn.clicked.connect(lambda: set_display_data(win, "fluorescence"))
    win.fluorescence_btn.setToolTip("Display fluorescence traces")

    # dF/F button
    win.dFoF_btn = QPushButton("dFoF")
    win.dFoF_btn.setStyleSheet(styles.roiBtnStyle())
    win.dFoF_btn.setFont(styles.roi_btn_font())
    win.dFoF_btn.clicked.connect(lambda: set_display_data(win, "dFoF"))
    win.dFoF_btn.setToolTip("Display dFoF traces")
    if parent.dFoF is None:
        win.dFoF_btn.setEnabled(False)

    # Processed dFoF button
    win.processed_dFoF_btn = QPushButton("Processed dFoF")
    win.processed_dFoF_btn.setStyleSheet(styles.roiBtnStyle())
    win.processed_dFoF_btn.setFont(styles.roi_btn_font())
    win.processed_dFoF_btn.clicked.connect(
        lambda: set_display_data(win, "processed_dFoF")
    )
    win.processed_dFoF_btn.setToolTip("Display processed dFoF traces")
    if parent.processed_dFoF is None:
        win.processed_dFoF_btn.setEnabled(False)

    # estimated spikes button
    win.spikes_btn = QPushButton("Spikes")
    win.spikes_btn.setStyleSheet(styles.roiBtnStyle())
    win.spikes_btn.setFont(styles.roi_btn_font())
    win.spikes_btn.clicked.connect(lambda: set_display_data(win, "Estimated Spikes"))
    win.spikes_btn.setToolTip("Display estimated spikes")
    if parent.deconvolved_spikes is None:
        win.spikes_btn.setEnabled(False)

    # volume button
    win.volume_btn = QPushButton("Volume")
    win.volume_btn.setStyleSheet(styles.roiBtnStyle())
    win.volume_btn.setFont(styles.roi_btn_font())
    win.volume_btn.clicked.connect(lambda: print("add function"))
    win.volume_btn.setToolTip("Show estimated spine volume plots")
    if parent.spine_volume is None:
        win.volume_btn.setEnabled(False)

    # Add buttons to frame
    control_layout.addWidget(win.fluorescence_btn)
    control_layout.addWidget(win.dFoF_btn)
    control_layout.addWidget(win.processed_dFoF_btn)
    control_layout.addWidget(win.spikes_btn)
    control_layout.addWidget(win.volume_btn)
    control_layout.addStretch(1)


def roi_list_display(parent, win):
    """Layout to display list of all the rois that can be selected to display
       in the plots"""

    # Make the layout
    roi_list_layout = QVBoxLayout()
    win.roi_list_display = QGroupBox(win, title="ROIs")
    win.roi_list_display.setStyleSheet(styles.roiFrameStyle())
    win.roi_list_display.setFont(styles.roi_btn_font())
    win.roi_list_display.setLayout(roi_list_layout)
    win.roi_list_display.setFixedWidth(120)

    win.roi_list = QListWidget()
    win.roi_list.setSelectionMode(QAbstractItemView.MultiSelection)
    win.roi_list.setStyleSheet(styles.roiListStyle())

    # Get the roi labels to display in the list
    # Grouping them so that spines will be adjacent to parent dendrite
    roi_labels = []
    if parent.parameters["Spine Groupings"]:
        spine_groupings = parent.parameters["Spine Groupings"]
    else:
        spine_groupings = [range(len(parent.ROIs["Spine"]))]
    for key, value in parent.dFoF.items():
        if key == "Soma":
            for i in range(np.shape(value)[1]):
                label = f"{key} {i+1}"
                roi_labels.append(label)
                item = QListWidgetItem(label)
                win.roi_list.addItem(item)
        if key == "Dendrite":
            for i in range(np.shape(value)[1]):
                label = f"{key} {i+1}"
                roi_labels.append(label)
                item = QListWidgetItem(label)
                win.roi_list.addItem(item)
                for j in spine_groupings[i]:
                    spine_label = f"Spine {j+1}"
                    roi_labels.append(spine_label)
                    item = QListWidgetItem(spine_label)
                    win.roi_list.addItem(item)
    win.roi_list.itemClicked.connect(lambda x: print(x))

    roi_list_layout.addWidget(win.roi_list)
    roi_list_layout.addStretch(1)
