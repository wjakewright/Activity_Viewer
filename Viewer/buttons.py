''' Module containing the buttons for Activity_Viewer GUI

    CREATOR
        William (Jake) Wright - 12/24/2021'''

from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout

def ROI_Buttons(parent):
    # Frame for the buttons
    roi_btn_layout = QVBoxLayout()
    parent.ROI_btn_box = QGroupBox(parent,title='Manage ROIs')
    parent.ROI_btn_box.setStyleSheet('''QGroupBox {
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
    parent.ROI_btn_box.setLayout(roi_btn_layout)
    parent.ROI_btn_box.setMinimumWidth(150)

    # Make buttons stylesheet
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

    # Make buttons
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

    # Add buttons to frame
    roi_btn_layout.addWidget(parent.draw_background_btn)
    roi_btn_layout.addWidget(parent.draw_dendrite_btn)
    roi_btn_layout.addWidget(parent.draw_spine_btn)
    roi_btn_layout.addWidget(parent.draw_soma_btn)

