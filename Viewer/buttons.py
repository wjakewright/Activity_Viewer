''' Module containing the buttons for Activity_Viewer GUI

    CREATOR
        William (Jake) Wright - 12/24/2021'''

from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QWidget

def ROI_Buttons(parent):
    # Main layout
    parent.roi_btn_widget = QWidget(parent)
    roi_btn_layout = QVBoxLayout()
    parent.roi_btn_widget.setLayout(roi_btn_layout)

    # Make buttons stylesheet
    roi_frame_style = ('''QGroupBox {
                                    font:bold;
                                    background:black;
                                    color:white;
                                    border:2px solid #132743;
                                    border-radius: 6px;
                                    margin-top: 6px}
                           QGroupBox::title {
                                    subcontrol-origin:margin;
                                    subcontrol-position:top;
                                    padding:0 3px 0 3px}''')
    roi_btn_style = ('''QPushButton {
                                     background:#132743;
                                     color:white;
                                     border-radius: 4px;
                                     text-align:center;
                                     border-style:outset;
                                     border-width: 0.5px;
                                     border-color:#24272D
                                     }
                        QPushButton:pressed {
                                     background:#02449B;
                                     color:white
                                     } ''')

    # --------------DRAW BUTTONS--------------
    # Frame for the draw buttons
    draw_btn_layout = QVBoxLayout()
    parent.draw_btn_box = QGroupBox(parent,title='Draw ROIs')
    parent.draw_btn_box.setStyleSheet(roi_frame_style)
    parent.draw_btn_box.setLayout(draw_btn_layout)
    parent.draw_btn_box.setMinimumWidth(150)

    ### Draw Background
    parent.draw_background_btn = QPushButton('Draw Background')
    parent.draw_background_btn.setStyleSheet(roi_btn_style)
    parent.draw_background_btn.setMinimumHeight(30)
    parent.draw_background_btn.clicked.connect(lambda: print('Add function'))
    ### Draw Dendrite
    parent.draw_dendrite_btn = QPushButton('Draw Dendrite')
    parent.draw_dendrite_btn.setStyleSheet(roi_btn_style)
    parent.draw_dendrite_btn.setMinimumHeight(30)
    parent.draw_dendrite_btn.clicked.connect(lambda: print('Add Function'))
    ### Draw Spine
    parent.draw_spine_btn = QPushButton('Draw Spine')
    parent.draw_spine_btn.setStyleSheet(roi_btn_style)
    parent.draw_spine_btn.setMinimumHeight(30)
    parent.draw_spine_btn.clicked.connect(lambda: print('Add Function'))
    ### Draw Soma
    parent.draw_soma_btn = QPushButton('Draw Soma')
    parent.draw_soma_btn.setStyleSheet(roi_btn_style)
    parent.draw_soma_btn.setMinimumHeight(30)
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
    parent.manage_btn_box.setLayout(manage_btn_layout)
    parent.manage_btn_box.setMinimumWidth(150)

    ### Draw Shift ROIs
    parent.shift_roi_btn = QPushButton('Shift ROIs')
    parent.shift_roi_btn.setStyleSheet(roi_btn_style)
    parent.shift_roi_btn.setMinimumHeight(30)
    parent.shift_roi_btn.clicked.connect(lambda: print('Add function'))

    ### Draw Edit ROIs
    parent.edit_roi_btn = QPushButton('Edit ROIs')
    parent.edit_roi_btn.setStyleSheet(roi_btn_style)
    parent.edit_roi_btn.setMinimumHeight(30)
    parent.edit_roi_btn.clicked.connect(lambda: print('Add function'))

    # Add manage buttons to manage frame
    manage_btn_layout.addWidget(parent.shift_roi_btn)
    manage_btn_layout.addWidget(parent.edit_roi_btn)

    # Add frames to main layout
    roi_btn_layout.addWidget(parent.draw_btn_box)
    roi_btn_layout.addWidget(parent.manage_btn_box)
    roi_btn_layout.addStretch()

