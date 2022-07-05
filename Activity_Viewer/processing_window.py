"""Module for creating the processing window after fluorescence trace extractin"""

import cmapy
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDesktopWidget,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from Activity_Viewer import signal_processing, styles


class Processing_Window(QDialog):
    """Custom window to display extracted raw fluorescent traces with inputs
        to specify how to further process the traces"""

    def __init__(self, parent):
        super(Processing_Window, self).__init__(parent=parent)
        self.parent = parent

        # Set up the window properties
        pg.setConfigOptions(imageAxisOrder="row-major")
        screen_size = QDesktopWidget().screenGeometry()
        win_h = int(screen_size.height() * 0.7)
        win_w = int(screen_size.width() * 0.7)
        self.setGeometry(70, 70, win_w, win_h)
        self.setWindowTitle("Process Fluorescence Traces")

        self.initWindow()

    def initWindow(self):
        """Putting everything into the window"""

        # Set up the grid layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Make processing parameters window
        parameters_window(self.parent, self)

        # Make spine grouping panel
        grouping_panel(self.parent, self)

        # Make ROI list view
        roi_list_window(self.parent, self)

        # Make buttons
        processing_buttons(self.parent, self)

        # Make the side panel display
        self.side_panel = QWidget()
        side_panel_layout = QVBoxLayout()
        self.side_panel.setLayout(side_panel_layout)
        self.side_panel.setFixedWidth(210)
        side_panel_layout.addWidget(self.param_widget)
        try:
            side_panel_layout.addWidget(self.grouping_frame)
        except AttributeError:
            pass
        side_panel_layout.addWidget(self.roi_list_frame)
        side_panel_layout.addWidget(self.btn_box)

        # Make the plot Window
        self.rois_to_plot = []
        self.roi_plots = {}
        generate_roi_plots(self.parent, self)
        self.plot = pg.PlotItem()
        self.plot.setTitle("Raw Fluorescence")
        self.plot.setMouseEnabled(y=False)
        # self.legend = pg.LegendItem(brush=pg.mkBrush((166, 160, 150, 0.5)))
        # self.legend.setParentItem(self.plot)
        self.plot.addLegend(
            labelTextColor=(255, 255, 255), brush=pg.mkBrush((0, 0, 0, 150))
        )
        self.plot_win = pg.PlotWidget(self, plotItem=self.plot)

        # Add items to grid layout
        self.grid_layout.addWidget(self.side_panel, 0, 0)
        self.grid_layout.addWidget(self.plot_win, 0, 1)

    def close_window(self):
        """Function to close window"""
        self.close()


def parameters_window(parent, win):
    """Make the processing parameters panel widget"""
    param_layout = QVBoxLayout()
    win.param_widget = QGroupBox(win, title="Parameters")
    win.param_widget.setStyleSheet(styles.roiFrameStyle())
    win.param_widget.setFont(styles.roi_btn_font())
    win.param_widget.setLayout(param_layout)
    win.param_widget.setFixedWidth(200)

    # ------------ ADD INPUTS-------------
    # Calculate dFoF
    win.dFoF_check_bx = QCheckBox("Calulate dFoF", parent=win)
    win.dFoF_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.dFoF_check_bx.setFont(styles.roi_btn_font())
    win.dFoF_check_bx.setToolTip("Check to calculate dFoF")
    win.dFoF_check_bx.setChecked(True)

    # Deconvolve
    win.deconvolve_check_bx = QCheckBox("Deconvolve Trace", parent=win)
    win.deconvolve_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.deconvolve_check_bx.setFont(styles.roi_btn_font())
    win.deconvolve_check_bx.setToolTip("Check to deconvolve traces")

    # Calculate Volume
    win.volume_check_bx = QCheckBox("Calculate Volume", parent=win)
    win.volume_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.volume_check_bx.setFont(styles.roi_btn_font())
    win.volume_check_bx.setToolTip("Check to calculate spine volume")

    # Correct bout separations
    win.bout_sep_check_bx = QCheckBox("Correct Bout Separations", parent=win)
    win.bout_sep_check_bx.setStyleSheet(styles.parameterCheckBoxStyle())
    win.bout_sep_check_bx.setFont(styles.roi_btn_font())
    win.bout_sep_check_bx.setToolTip(
        "Check to correct separations between imaging bouts"
    )

    # Downsample window
    win.ds_label = QLabel("Downsample Ratio")
    win.ds_label.setStyleSheet(styles.parameterLabelStyle())
    win.ds_label.setFont(styles.parameterLabelFont())
    win.ds_win_input = QLineEdit()
    win.ds_win_input.setStyleSheet(styles.parameterInputStyle())
    win.ds_win_input.setFont(styles.roi_btn_font())
    win.ds_win_input.setText("20")
    win.ds_win_input.setToolTip("Frames to downsample for baseline estimation")

    # Smooth Window
    win.smooth_label = QLabel("Smooth Window")
    win.smooth_label.setStyleSheet(styles.parameterLabelStyle())
    win.smooth_label.setFont(styles.parameterLabelFont())
    win.smooth_win_input = QLineEdit()
    win.smooth_win_input.setStyleSheet(styles.parameterInputStyle())
    win.smooth_win_input.setFont(styles.roi_btn_font())
    if parent.imaging_sensor == "iGluSnFr3" or parent.imaging_sensor == "RCaMP2":
        default_smooth = "0.5"
    else:
        default_smooth = "0.0"
    win.smooth_win_input.setText(default_smooth)
    win.smooth_win_input.setToolTip("Window to smooth trace over in processing")

    win.thresh_label = QLabel("Event Threshold")
    win.thresh_label.setStyleSheet(styles.parameterLabelStyle())
    win.thresh_label.setFont(styles.parameterLabelFont())
    win.thresh_input = QLineEdit()
    win.thresh_input.setStyleSheet(styles.parameterInputStyle())
    win.thresh_input.setFont(styles.roi_btn_font())
    if parent.imaging_sensor == "iGluSnFr3" or parent.imaging_sensor == "RCaMP2":
        default_thresh = "2"
    else:
        default_thresh = "3"
    win.thresh_input.setText(default_thresh)
    win.thresh_input.setToolTip("Threshold multiplier for event detection over noise")

    # Artifact Frames
    win.artifact_label = QLabel("Artifact Frames")
    win.artifact_label.setStyleSheet(styles.parameterLabelStyle())
    win.artifact_label.setFont(styles.parameterLabelFont())
    win.artifact_input = QLineEdit()
    win.artifact_input.setStyleSheet(styles.parameterInputStyle())
    win.artifact_input.setFont(styles.roi_btn_font())
    win.artifact_sublabel = QLabel("e.g., 10-40;80-100")
    win.artifact_sublabel.setStyleSheet(styles.parameterSubLabelStyle())
    win.artifact_sublabel.setFont(styles.parameterSubLabelFont())
    win.artifact_input.setToolTip("Frames to correct for large artifacts")

    # Add inputs to layout
    param_layout.addWidget(win.dFoF_check_bx)
    param_layout.addWidget(win.deconvolve_check_bx)
    param_layout.addWidget(win.volume_check_bx)
    param_layout.addWidget(win.bout_sep_check_bx)
    param_layout.addWidget(win.ds_label)
    param_layout.addWidget(win.ds_win_input)
    param_layout.addWidget(win.smooth_label)
    param_layout.addWidget(win.smooth_win_input)
    param_layout.addWidget(win.thresh_label)
    param_layout.addWidget(win.thresh_input)
    param_layout.addWidget(win.artifact_label)
    param_layout.addWidget(win.artifact_input)
    param_layout.addWidget(win.artifact_sublabel)
    param_layout.addStretch(1)


def grouping_panel(parent, win):
    """Layout to display inputs for spine groupings"""
    # Determine if spine grouping is necessary
    try:
        dend_num = np.shape(parent.ROI_fluorescence["Dendrite"])[1]
    except:
        return

    if dend_num < 2 or "Spine" not in parent.ROI_fluorescence:
        return

    # Making the grouping layout
    grouping_layout = QVBoxLayout()
    win.grouping_frame = QGroupBox(win, title="Spine Groupings")
    win.grouping_frame.setStyleSheet(styles.roiFrameStyle())
    win.grouping_frame.setFont(styles.roi_btn_font())
    win.grouping_frame.setLayout(grouping_layout)
    win.grouping_frame.setFixedWidth(200)

    # Make grouping input for each dendrite
    win.grouping_label_list = []
    win.grouping_input_list = []
    for i in range(dend_num):
        label = QLabel(f"Dendrite {i+1}")
        label.setStyleSheet(styles.parameterLabelStyle())
        label.setFont(styles.parameterLabelFont())
        win.grouping_label_list.append(label)
        input = QLineEdit()
        input.setPlaceholderText("Enter spines on this dendrite")
        input.setStyleSheet(styles.parameterInputStyle())
        input.setFont(styles.roi_btn_font())
        input.setToolTip("Specify which spines belong to this dendrite")
        win.grouping_input_list.append(input)
        grouping_layout.addWidget(win.grouping_label_list[i])
        grouping_layout.addWidget(win.grouping_input_list[i])

    grouping_sub_label = QLabel("e.g., 1-15")
    grouping_sub_label.setStyleSheet(styles.parameterSubLabelStyle())
    grouping_sub_label.setFont(styles.parameterSubLabelFont())

    # Add input items to the layout
    grouping_layout.addWidget(grouping_sub_label)
    grouping_layout.addStretch(1)


def roi_list_window(parent, win):
    """Layout to display list of all rois that can be selected
        to display in the plot"""
    # Make the layout
    roi_list_layout = QVBoxLayout()
    win.roi_list_frame = QGroupBox(win, title="ROIs")
    win.roi_list_frame.setStyleSheet(styles.roiFrameStyle())
    win.roi_list_frame.setFont(styles.roi_btn_font())
    win.roi_list_frame.setLayout(roi_list_layout)
    win.roi_list_frame.setFixedWidth(200)

    win.ROI_list_window = QListWidget()
    win.ROI_list_window.setSelectionMode(QAbstractItemView.MultiSelection)
    win.ROI_list_window.setStyleSheet(styles.roiListStyle())

    # Get the ROI labels to display
    roi_labels = []
    for key, value in parent.ROIs.items():
        if not value:
            continue
        for i, _ in enumerate(value):
            label = f"{key} {i+1}"
            roi_labels.append(label)
            item = QListWidgetItem(label)
            win.ROI_list_window.addItem(item)
    win.ROI_list_window.itemClicked.connect(lambda x: plot_roi(parent, win, x))

    roi_list_layout.addWidget(win.ROI_list_window)
    roi_list_layout.addStretch(1)


def processing_buttons(parent, win):
    """Make processing buttons"""

    # Make button layout
    btn_layout = QHBoxLayout()
    win.btn_box = QGroupBox(win)
    # win.btn_box.setStyleSheet(styles.roiFrameStyle())
    win.btn_box.setLayout(btn_layout)
    win.btn_box.setFixedWidth(200)

    # Processing Button
    win.process_btn = QPushButton("Process")
    win.process_btn.setStyleSheet(styles.roiBtnStyle())
    win.process_btn.setFont(styles.roi_btn_font())
    win.process_btn.clicked.connect(
        lambda: signal_processing.process_traces(parent, win)
    )
    win.process_btn.setToolTip("Process Traces")

    # Cancel Button
    win.cancel_btn = QPushButton("Cancel")
    win.cancel_btn.setStyleSheet(styles.roiBtnStyle())
    win.cancel_btn.setFont(styles.roi_btn_font())
    win.cancel_btn.clicked.connect(lambda: win.close_window())
    win.cancel_btn.setToolTip("Cancel Processing")

    btn_layout.addWidget(win.process_btn)
    btn_layout.addWidget(win.cancel_btn)


def generate_roi_plots(parent, win):
    """Functon to make all the plot data items for each roi"""
    # colors = np.uint8(np.random.randint(0, 255, size=(win.ROI_list_window.count(), 3)))
    c_i = np.linspace(0, 256, win.ROI_list_window.count(), dtype=int)
    colors = [
        cmapy.color("jet", c_i[i], rgb_order=True)
        for i in range(win.ROI_list_window.count())
    ]
    c_idx = 0
    for n, (key, value) in enumerate(parent.ROI_fluorescence.items()):
        if key != "Dendrite Poly":
            win.roi_plots[key] = []
            for i in range(np.shape(value)[1]):
                p = pg.PlotDataItem(value[:, i], name=f"{key} {i+1}")
                p.setPen(pg.mkPen(tuple(colors[c_idx]), width=1))
                win.roi_plots[key].append(p)
                c_idx = c_idx + 1


def plot_roi(parent, win, roi):
    # Function to add roi plots to plot window when they are selected
    roi = roi.text()
    if roi not in win.rois_to_plot:
        win.rois_to_plot.append(roi)
    else:
        win.rois_to_plot.remove(roi)

    update_plot(parent, win)


def update_plot(parent, win):
    """Function to update the plot window"""
    win.plot.clear()

    for i, roi in enumerate(win.rois_to_plot):
        key, idx = roi.split(" ")
        idx = int(idx)
        plot = win.roi_plots[key][idx - 1]
        new_data = parent.ROI_fluorescence[key][:, idx - 1]
        dmin = new_data.min()
        dmax = new_data.max()
        new_data = (new_data - dmin) / (dmax - dmin)
        new_data = new_data + (i)
        plot.setData(new_data)
        win.plot.addItem(plot)

