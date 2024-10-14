"""Module for creating window to visualize the final outputs after processing"""

import cmapy
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDesktopWidget,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from Activity_Viewer import messages, output, styles


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
        self.rois_to_plot = []

        # Set up grid layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Make data display control frame
        display_control_window(self.parent, self)

        # Make roi list display
        roi_list_display(self.parent, self)

        # Make buttons
        final_buttons(self.parent, self)

        # Make ROI plots
        self.roi_plots, self.roi_data = make_roi_plots(self.parent, self)

        # Make the side panel display
        self.side_panel = QWidget()
        side_panel_layout = QVBoxLayout()
        self.side_panel.setLayout(side_panel_layout)
        self.side_panel.setFixedWidth(130)
        side_panel_layout.addWidget(self.control_widget)
        side_panel_layout.addWidget(self.roi_list_display)
        side_panel_layout.addWidget(self.btn_box)
        side_panel_layout.addStretch(1)

        # Make the plot area
        self.plot_window = QWidget()
        self.plot_window_layout = QGridLayout()
        self.plot_window.setLayout(self.plot_window_layout)

        # Add items to the grid layout
        self.grid_layout.addWidget(self.side_panel, 0, 0)
        self.grid_layout.addWidget(self.plot_window, 0, 1)

    def closeEvent(self, event):
        """Function to prompt saving when closing the window"""
        messages.save_output_warning(self.parent)

        event.accept()


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
    update_roi_plots(win)


def make_roi_plots(parent, win):
    """Function to make all the roi plots"""
    # Make colors
    c_i = np.linspace(0, 256, win.roi_list.count(), dtype=int)
    colors = [
        cmapy.color("jet", c_i[i], rgb_order=True) for i in range(win.roi_list.count())
    ]

    roi_plots = {"Fluorescence": []}
    roi_data = {"Fluorescence": []}
    if parent.dFoF is not None:
        roi_plots["dFoF"] = []
        roi_plots["Processed dFoF"] = []
        roi_data["dFoF"] = []
        roi_data["Processed dFoF"] = []
    if parent.deconvolved_spikes is not None:
        roi_plots["Estimated Spikes"] = []
        roi_data["Estimated Spikes"] = []

    rois = [win.roi_list.item(x).text() for x in range(win.roi_list.count())]
    c_idx = 0
    for roi in rois:
        # for fluorescence
        roi_type, idx = roi.split(" ")
        idx = int(idx) - 1
        if parent.fluorescence_processed is not None:
            data = parent.fluorescence_processed[roi_type][:, idx]
            data = (data - data.min()) / (data.max() - data.min())
            p = pg.PlotDataItem(data, name=f"{roi_type} {idx+1}")
            p.setPen(pg.mkPen(tuple(colors[c_idx]), width=1))
            roi_plots["Fluorescence"].append(p)
            roi_data["Fluorescence"].append(data)
        # for dFoF
        if parent.dFoF is not None:
            data_d = parent.dFoF[roi_type][:, idx]
            data_d = (data_d - data_d.min()) / (data_d.max() - data_d.min())
            d = pg.PlotDataItem(data_d, name=f"{roi_type} {idx+1}")
            d.setPen(pg.mkPen(tuple(colors[c_idx]), width=1))
            roi_plots["dFoF"].append(d)
            roi_data["dFoF"].append(data_d)

            data_p = parent.processed_dFoF[roi_type][:, idx]
            data_p = (data_p - data_p.min()) / (data_p.max() - data_p.min())
            pd = pg.PlotDataItem(data_p, name=f"{roi_type} {idx+1}")
            pd.setPen(pg.mkPen(tuple(colors[c_idx]), width=1))
            roi_plots["Processed dFoF"].append(pd)
            roi_data["Processed dFoF"].append(data_p)
        # For estimated spikes
        if parent.deconvolved_spikes is not None:
            data_s = parent.deconvolved_spikes[roi_type][:, idx]
            data_s = (data_s - data_s.min()) / (data_s.max() - data_s.min())
            s = pg.PlotDataItem(data_s, name=f"{roi_type} {idx+1}")
            s.setPen(pg.mkPen(tuple(colors[c_idx]), width=1))
            roi_plots["Estimated Spikes"].append(s)
            roi_data["Estimated Spikes"].append(data_s)
        c_idx = c_idx + 1

    return roi_plots, roi_data


def add_roi_plots(parent, win, roi):
    """Function to add rois to the plots"""
    idx = win.roi_list.row(roi)
    if idx not in win.rois_to_plot:
        win.rois_to_plot.append(idx)
    else:
        win.rois_to_plot.remove(idx)

    win.rois_to_plot.sort()

    update_roi_plots(win)


def update_roi_plots(win):
    """Function to update the plots with new roi data"""
    for plt in win.plot_widgets:
        plt.clear()
        d_type = plt.getPlotItem().titleLabel.text
        for i, idx in enumerate(win.rois_to_plot):
            plot = win.roi_plots[d_type][idx]
            data = np.array(win.roi_data[d_type][idx]) + i
            plot.setData(data)
            plt.getPlotItem().addItem(plot)


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
    win.fluorescence_btn.clicked.connect(lambda: set_display_data(win, "Fluorescence"))
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
        lambda: set_display_data(win, "Processed dFoF")
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
    for key, value in parent.ROI_fluorescence.items():
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
    win.roi_list.itemClicked.connect(lambda x: add_roi_plots(parent, win, x))

    roi_list_layout.addWidget(win.roi_list)
    roi_list_layout.addStretch(1)


def final_buttons(parent, win):
    """Make buttons to save or reject final outputs"""

    # Make button layout
    btn_layout = QHBoxLayout()
    win.btn_box = QGroupBox(win)
    win.btn_box.setLayout(btn_layout)
    win.btn_box.setFixedWidth(120)

    # Save results button
    win.save_results_btn = QPushButton("Save")
    win.save_results_btn.setStyleSheet(styles.roiBtnStyle())
    win.save_results_btn.setFont(styles.roi_btn_font())
    win.save_results_btn.clicked.connect(lambda: output.output_data(parent))
    win.save_results_btn.setToolTip("Save Results")

    # Cancel Button
    win.cancel_btn = QPushButton("Cancel")
    win.cancel_btn.setStyleSheet(styles.roiBtnStyle())
    win.cancel_btn.setFont(styles.roi_btn_font())
    win.cancel_btn.clicked.connect(lambda: print("Add function"))
    win.cancel_btn.setToolTip("Cancel Exporting")

    btn_layout.addWidget(win.save_results_btn)
    btn_layout.addWidget(win.cancel_btn)
