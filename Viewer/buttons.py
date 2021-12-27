''' Module containing the buttons for Activity_Viewer GUI

    CREATOR
        William (Jake) Wright - 12/24/2021'''

from PyQt5.QtWidgets import (QGroupBox, QPushButton, QScrollBar, QVBoxLayout, QWidget,
                             QHBoxLayout)
from PyQt5.QtCore import Qt
import styles
import display

def ROI_Buttons(parent):
    # Main layout
    parent.roi_btn_widget = QWidget(parent)
    roi_btn_layout = QVBoxLayout()
    parent.roi_btn_widget.setLayout(roi_btn_layout)

    # Make buttons stylesheet
    roi_frame_style = styles.roiFrameStyle()
    roi_frame_font = styles.roi_btn_font(bold=True)
    roi_btn_style = styles.roiBtnStyle()
    roi_btn_font = styles.roi_btn_font()

    # --------------DRAW BUTTONS--------------
    # Frame for the draw buttons
    draw_btn_layout = QVBoxLayout()
    parent.draw_btn_box = QGroupBox(parent,title='Draw ROIs')
    parent.draw_btn_box.setStyleSheet(roi_frame_style)
    parent.draw_btn_box.setFont(roi_frame_font)
    parent.draw_btn_box.setLayout(draw_btn_layout)
    parent.draw_btn_box.setMinimumWidth(120)

    ### Draw Background
    parent.draw_background_btn = QPushButton('Background')
    parent.draw_background_btn.setStyleSheet(roi_btn_style)
    parent.draw_background_btn.setMinimumHeight(25)
    parent.draw_background_btn.setFont(roi_btn_font)
    parent.draw_background_btn.clicked.connect(lambda: print('Add function'))
    ### Draw Dendrite
    parent.draw_dendrite_btn = QPushButton('Dendrite')
    parent.draw_dendrite_btn.setStyleSheet(roi_btn_style)
    parent.draw_dendrite_btn.setMinimumHeight(25)
    parent.draw_dendrite_btn.setFont(roi_btn_font)
    parent.draw_dendrite_btn.clicked.connect(lambda: print('Add Function'))
    ### Draw Spine
    parent.draw_spine_btn = QPushButton('Spine')
    parent.draw_spine_btn.setStyleSheet(roi_btn_style)
    parent.draw_spine_btn.setMinimumHeight(25)
    parent.draw_spine_btn.setFont(roi_btn_font)
    parent.draw_spine_btn.clicked.connect(lambda: print('Add Function'))
    ### Draw Soma
    parent.draw_soma_btn = QPushButton('Soma')
    parent.draw_soma_btn.setStyleSheet(roi_btn_style)
    parent.draw_soma_btn.setMinimumHeight(25)
    parent.draw_soma_btn.setFont(roi_btn_font)
    parent.draw_soma_btn.clicked.connect(lambda: print('Add function'))

    # Add draw buttons to draw frame
    draw_btn_layout.addWidget(parent.draw_background_btn)
    draw_btn_layout.addWidget(parent.draw_dendrite_btn)
    draw_btn_layout.addWidget(parent.draw_spine_btn)
    draw_btn_layout.addWidget(parent.draw_soma_btn)
    draw_btn_layout.addStretch()

    #---------------MANAGE BUTTONS-----------------
    # Frame for the draw buttons
    manage_btn_layout = QVBoxLayout()
    parent.manage_btn_box = QGroupBox(parent,title='Manage ROIs')
    parent.manage_btn_box.setStyleSheet(roi_frame_style)
    parent.manage_btn_box.setFont(roi_frame_font)
    parent.manage_btn_box.setLayout(manage_btn_layout)
    parent.manage_btn_box.setMinimumWidth(120)

    ### Select ROIs
    parent.select_roi_btn = QPushButton('Select ROIs')
    parent.select_roi_btn.setStyleSheet(roi_btn_style)
    parent.select_roi_btn.setMinimumHeight(25)
    parent.select_roi_btn.setFont(roi_btn_font)
    parent.select_roi_btn.clicked.connect(lambda: print('Add function'))

    ### Shift ROIs
    parent.shift_roi_btn = QPushButton('Shift ROIs')
    parent.shift_roi_btn.setStyleSheet(roi_btn_style)
    parent.shift_roi_btn.setMinimumHeight(25)
    parent.shift_roi_btn.setFont(roi_btn_font)
    parent.shift_roi_btn.clicked.connect(lambda: print('Add function'))

    ### Edit ROIs
    parent.edit_roi_btn = QPushButton('Edit ROIs')
    parent.edit_roi_btn.setStyleSheet(roi_btn_style)
    parent.edit_roi_btn.setMinimumHeight(25)
    parent.edit_roi_btn.setFont(roi_btn_font)
    parent.edit_roi_btn.clicked.connect(lambda: print('Add function'))

    ### Delete ROIs
    parent.delete_roi_btn = QPushButton('Delete ROIs')
    parent.delete_roi_btn.setStyleSheet(roi_btn_style)
    parent.delete_roi_btn.setMinimumHeight(25)
    parent.delete_roi_btn.setFont(roi_btn_font)
    parent.delete_roi_btn.clicked.connect(lambda: print('add function'))

    ### Extract ROIs
    parent.extract_roi_btn = QPushButton('Extract ROIs')
    parent.extract_roi_btn.setStyleSheet(roi_btn_style)
    parent.extract_roi_btn.setMinimumHeight(25)
    parent.extract_roi_btn.setFont(roi_btn_font)
    parent.extract_roi_btn.clicked.connect(lambda: print('add function'))

    ### Display ROIs
    parent.display_roi_btn = QPushButton('Display ROIs')
    parent.display_roi_btn.setStyleSheet(roi_btn_style)
    parent.display_roi_btn.setMinimumHeight(25)
    parent.display_roi_btn.setFont(roi_btn_font)
    parent.display_roi_btn.clicked.connect(lambda: print('add function'))


    # Add manage buttons to manage frame
    manage_btn_layout.addWidget(parent.select_roi_btn)
    manage_btn_layout.addWidget(parent.shift_roi_btn)
    manage_btn_layout.addWidget(parent.edit_roi_btn)
    manage_btn_layout.addWidget(parent.delete_roi_btn)
    manage_btn_layout.addWidget(parent.extract_roi_btn)
    manage_btn_layout.addWidget(parent.display_roi_btn)

    # Add frames to main layout
    roi_btn_layout.addWidget(parent.draw_btn_box)
    roi_btn_layout.addWidget(parent.manage_btn_box)
    roi_btn_layout.addStretch()


def image_slider(parent):
    parent.slider_widget = QWidget(parent)
    parent.slider_layout = QHBoxLayout()
    parent.slider_widget.setLayout(parent.slider_layout)
    parent.play_btn = QPushButton('➤')
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


