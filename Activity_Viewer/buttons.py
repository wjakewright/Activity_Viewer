""" Module containing the buttons for Activity_Viewer GUI

    CREATOR
        William (Jake) Wright - 12/24/2021"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollBar,
    QVBoxLayout,
    QWidget,
)

from Activity_Viewer import ROIs, display, signal_extraction, styles


def ROI_Buttons(parent):
    # Main layout
    parent.roi_btn_widget = QWidget(parent)
    roi_btn_layout = QVBoxLayout()
    parent.roi_btn_widget.setLayout(roi_btn_layout)
    parent.roi_btn_widget.setFixedWidth(140)

    # Make buttons stylesheet
    roi_frame_style = styles.roiFrameStyle()
    roi_frame_font = styles.roi_btn_font(bold=True)
    roi_btn_style = styles.roiBtnStyle()
    roi_btn_font = styles.roi_btn_font()
    parameter_field_style = styles.parameterInputStyle()
    parameter_label_style = styles.parameterLabelStyle()
    sensor_input_style = styles.sensorInputStyle()

    # --------------DRAW BUTTONS--------------
    # Frame for the draw buttons
    draw_btn_layout = QVBoxLayout()
    parent.draw_btn_box = QGroupBox(parent, title="Draw ROIs")
    parent.draw_btn_box.setStyleSheet(roi_frame_style)
    parent.draw_btn_box.setFont(roi_frame_font)
    parent.draw_btn_box.setLayout(draw_btn_layout)
    parent.draw_btn_box.setFixedWidth(130)

    ### Draw Background
    parent.draw_background_btn = QPushButton("Background")
    parent.draw_background_btn.setStyleSheet(roi_btn_style)
    parent.draw_background_btn.setFixedHeight(20)
    parent.draw_background_btn.setFont(roi_btn_font)
    parent.draw_background_btn.clicked.connect(
        lambda: ROIs.Trigger_Background_ROI(parent, parent.display_image)
    )
    parent.draw_background_btn.setToolTip("Draw Background ROI")
    ### Draw Dendrite
    parent.draw_dendrite_btn = QPushButton("Dendrite")
    parent.draw_dendrite_btn.setStyleSheet(roi_btn_style)
    parent.draw_dendrite_btn.setFixedHeight(20)
    parent.draw_dendrite_btn.setFont(roi_btn_font)
    parent.draw_dendrite_btn.clicked.connect(
        lambda: ROIs.Trigger_Dendrite_ROI(parent, parent.display_image)
    )
    parent.draw_dendrite_btn.setToolTip("Draw Dendrite ROI")
    ### Draw Spine
    parent.draw_spine_btn = QPushButton("Spine")
    parent.draw_spine_btn.setStyleSheet(roi_btn_style)
    parent.draw_spine_btn.setFixedHeight(20)
    parent.draw_spine_btn.setFont(roi_btn_font)
    parent.draw_spine_btn.clicked.connect(
        lambda: ROIs.Trigger_Spine_ROI(parent, parent.display_image)
    )
    parent.draw_spine_btn.setToolTip("Draw Spine ROI")
    ### Draw Soma
    parent.draw_soma_btn = QPushButton("Soma")
    parent.draw_soma_btn.setStyleSheet(roi_btn_style)
    parent.draw_soma_btn.setFixedHeight(20)
    parent.draw_soma_btn.setFont(roi_btn_font)
    parent.draw_soma_btn.clicked.connect(
        lambda: ROIs.Trigger_Soma_ROI(parent, parent.display_image)
    )
    parent.draw_soma_btn.setToolTip("Draw Soma ROI")

    # Add draw buttons to draw frame
    draw_btn_layout.addWidget(parent.draw_background_btn)
    draw_btn_layout.addWidget(parent.draw_dendrite_btn)
    draw_btn_layout.addWidget(parent.draw_spine_btn)
    draw_btn_layout.addWidget(parent.draw_soma_btn)
    draw_btn_layout.addStretch(1)
    draw_btn_layout.setSpacing(7)

    # ---------------MANAGE BUTTONS-----------------
    # Frame for the draw buttons
    manage_btn_layout = QVBoxLayout()
    parent.manage_btn_box = QGroupBox(parent, title="Manage ROIs")
    parent.manage_btn_box.setStyleSheet(roi_frame_style)
    parent.manage_btn_box.setFont(roi_frame_font)
    parent.manage_btn_box.setLayout(manage_btn_layout)
    parent.manage_btn_box.setFixedWidth(130)

    ### Select ROIs
    parent.select_roi_btn = QPushButton("Select ROIs")
    parent.select_roi_btn.setStyleSheet(roi_btn_style)
    parent.select_roi_btn.setFixedHeight(20)
    parent.select_roi_btn.setFont(roi_btn_font)
    parent.select_roi_btn.clicked.connect(lambda: ROIs.to_select_ROIs(parent))
    parent.select_roi_btn.setToolTip("Select ROIs")

    ### Shift ROIs
    parent.shift_roi_btn = QPushButton("Shift ROIs")
    parent.shift_roi_btn.setStyleSheet(roi_btn_style)
    parent.shift_roi_btn.setFixedHeight(20)
    parent.shift_roi_btn.setFont(roi_btn_font)
    parent.shift_roi_btn.clicked.connect(lambda: ROIs.to_shift_ROIs(parent))
    parent.shift_roi_btn.setToolTip("Shift all ROIs together")

    ### Label ROIs
    parent.label_roi_btn = QPushButton("Label ROIs")
    parent.label_roi_btn.setStyleSheet(roi_btn_style)
    parent.label_roi_btn.setFixedHeight(20)
    parent.label_roi_btn.setFont(roi_btn_font)
    parent.label_roi_btn.clicked.connect(lambda: ROIs.toggle_ROI_labels(parent))
    parent.label_roi_btn.setToolTip("Toggle ROI label display")

    ### Flag ROIs
    parent.flag_roi_btn = QPushButton("Flag ROIs")
    parent.flag_roi_btn.setStyleSheet(roi_btn_style)
    parent.flag_roi_btn.setFixedHeight(20)
    parent.flag_roi_btn.setFont(roi_btn_font)
    parent.flag_roi_btn.clicked.connect(lambda: ROIs.to_flag_ROIs(parent))
    parent.flag_roi_btn.setToolTip("Add descriptive flag to ROI")

    ### Delete ROIs
    parent.delete_roi_btn = QPushButton("Delete ROIs")
    parent.delete_roi_btn.setStyleSheet(roi_btn_style)
    parent.delete_roi_btn.setFixedHeight(20)
    parent.delete_roi_btn.setFont(roi_btn_font)
    parent.delete_roi_btn.clicked.connect(lambda: ROIs.to_delete_ROIs(parent))
    parent.delete_roi_btn.setToolTip("Select and Delete ROIs")

    ### Clear ROIs
    parent.clear_roi_btn = QPushButton("Clear ROIs")
    parent.clear_roi_btn.setStyleSheet(roi_btn_style)
    parent.clear_roi_btn.setFixedHeight(20)
    parent.clear_roi_btn.setFont(roi_btn_font)
    parent.clear_roi_btn.clicked.connect(lambda: ROIs.to_clear_ROIs(parent))
    parent.clear_roi_btn.setToolTip("Clears all ROIs")

    ### Save ROIs
    parent.save_roi_btn = QPushButton("Save ROIs")
    parent.save_roi_btn.setStyleSheet(roi_btn_style)
    parent.save_roi_btn.setFixedHeight(20)
    parent.save_roi_btn.setFont(roi_btn_font)
    parent.save_roi_btn.clicked.connect(lambda: ROIs.save_ROIs(parent))
    parent.save_roi_btn.setToolTip("Save ROIs masks")

    ### Extract Traces
    parent.extract_roi_btn = QPushButton("Extract Traces")
    parent.extract_roi_btn.setStyleSheet(roi_btn_style)
    parent.extract_roi_btn.setFixedHeight(20)
    parent.extract_roi_btn.setFont(roi_btn_font)
    parent.extract_roi_btn.clicked.connect(
        lambda: signal_extraction.extract_raw_fluorescence(parent)
    )
    parent.extract_roi_btn.setToolTip("Extract ROI fluorescence")

    # Add manage buttons to manage frame
    manage_btn_layout.addWidget(parent.select_roi_btn)
    manage_btn_layout.addWidget(parent.shift_roi_btn)
    manage_btn_layout.addWidget(parent.label_roi_btn)
    manage_btn_layout.addWidget(parent.flag_roi_btn)
    manage_btn_layout.addWidget(parent.delete_roi_btn)
    manage_btn_layout.addWidget(parent.clear_roi_btn)
    manage_btn_layout.addWidget(parent.save_roi_btn)
    manage_btn_layout.addWidget(parent.extract_roi_btn)
    manage_btn_layout.addStretch(1)
    manage_btn_layout.setSpacing(7)

    # -------------PARAMETER INPUTS--------------
    parameters_layout = QVBoxLayout()
    parent.parameters_box = QGroupBox(parent, title="Parameters")
    parent.parameters_box.setStyleSheet(roi_frame_style)
    parent.parameters_box.setFont(roi_frame_font)
    parent.parameters_box.setLayout(parameters_layout)
    parent.parameters_box.setFixedWidth(130)

    ### Sensor Info
    parent.sensor_input = QComboBox()
    parent.sensor_input.addItems(parent.sensor_list)
    parent.sensor_input.setStyleSheet(sensor_input_style)
    parent.sensor_input.currentIndexChanged.connect(lambda: sensor_selection(parent))
    parent.sensor_input_label = QLabel("Imaging Sensor")
    parent.sensor_input_label.setStyleSheet(parameter_label_style)
    parent.sensor_input_label.setFont(styles.parameterLabelFont())

    ### Zoom Magnitude
    parent.zoom_input = QLineEdit()
    parent.zoom_input.setPlaceholderText("Enter Zoom")
    parent.zoom_input.setStyleSheet(parameter_field_style)
    parent.zoom_input.setFont(roi_btn_font)
    parent.zoom_input_label = QLabel("Zoom Value")
    parent.zoom_input_label.setStyleSheet(parameter_label_style)
    parent.zoom_input_label.setFont(styles.parameterLabelFont())

    ### Imaging Rate
    parent.image_rate_input = QLineEdit()
    parent.image_rate_input.setPlaceholderText("Enter Rate")
    parent.image_rate_input.setStyleSheet(parameter_field_style)
    parent.image_rate_input.setFont(roi_btn_font)
    parent.image_rate_input_label = QLabel("Imaging Rate")
    parent.image_rate_input_label.setStyleSheet(parameter_label_style)
    parent.image_rate_input_label.setFont(styles.parameterLabelFont())

    # Add inputs to the parameter frame
    parameters_layout.addWidget(parent.sensor_input_label)
    parameters_layout.addWidget(parent.sensor_input)
    parameters_layout.addWidget(parent.zoom_input_label)
    parameters_layout.addWidget(parent.zoom_input)
    parameters_layout.addWidget(parent.image_rate_input_label)
    parameters_layout.addWidget(parent.image_rate_input)

    # Add frames to main layout
    roi_btn_layout.addWidget(parent.draw_btn_box)
    roi_btn_layout.addWidget(parent.manage_btn_box)
    roi_btn_layout.addWidget(parent.parameters_box)
    roi_btn_layout.addStretch(1)


def image_slider(parent):
    parent.slider_widget = QWidget(parent)
    parent.slider_layout = QHBoxLayout()
    parent.slider_widget.setLayout(parent.slider_layout)
    parent.play_btn = QPushButton("➤")
    parent.play_btn.setStyleSheet(styles.playBtnStyle())
    parent.play_btn.setMaximumWidth(30)
    parent.play_btn.clicked.connect(lambda: display.Play_Video(parent))
    parent.image_slider = QScrollBar(Qt.Horizontal)
    parent.image_slider.setFocusPolicy(Qt.StrongFocus)
    parent.image_slider.setStyleSheet(styles.sliderStyle())
    parent.slider_layout.addWidget(parent.play_btn)
    parent.slider_layout.addWidget(parent.image_slider)
    parent.image_slider.setEnabled(False)
    parent.play_btn.setEnabled(False)


def sensor_selection(parent):
    sensor_idx = parent.sensor_input.currentIndex()
    parent.imaging_sensor = parent.sensor_list[sensor_idx]

