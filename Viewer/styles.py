""" Module containing all the styles for Activity_Viewer
    GUI widgets"""

from PyQt5.QtGui import QFont


def menuStyle():
    # Style for main menu bar
    menu_style = """QMenuBar {
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
                                color:white;}"""
    return menu_style


def sliderStyle():
    # Style for slider
    slider_style = """QScrollBar:horizontal {background-color:#131416;
                                              border: 1px solid #24272D;
                                              margin:0px 20px 0px 20px}
                       QScrollBar::handle:horizontal {background:#24272D;
                                                      color:white}
                       QScrollBar::add-line:horizontal {background:#24272D;
                                                        width:15px;
                                                        subcontrol-position: right;
                                                        subcontrol-origin: margin}
                       QScrollBar::sub-line:horizontal {background:#24272D;
                                                        width:15px;
                                                        subcontrol-position: left;
                                                        subcontrol-origin: margin}
                       QScrollBar:left-arrow:horizontal,QScrollBar:right-arrow:horizontal{
                                                        width:3px;
                                                        height:3px;
                                                        background:white}"""
    return slider_style


def roiFrameStyle():
    # Style for roi button frame
    roi_frame_style = """QGroupBox {
                                    font:bold;
                                    background:black;
                                    color:white;
                                    border:2px solid #132743;
                                    border-radius: 6px;
                                    margin-top: 6px}
                           QGroupBox::title {
                                    subcontrol-origin:margin;
                                    subcontrol-position:top;
                                    padding:0 3px 0 3px}"""
    return roi_frame_style


def roiBtnStyle():
    # Style for roi buttons
    roi_btn_style = """QPushButton {
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
                                     } """
    return roi_btn_style


def playBtnStyle():
    # Style for play button
    play_btn_style = """QPushButton {
                                      background:#131416;
                                      color:white;
                                      border-radius: 3px;
                                      text-align:center;
                                      border-style:outset;
                                      border-color:#24272D;
                                      border-width: 0.5px
                                      }
                         QPushButton:pressed {
                                      background:#24272D;
                                      color:white
                                      }"""
    return play_btn_style


def roi_btn_font(bold=False):
    # Font style for the ROI buttons
    if bold is False:
        roi_btn_font = QFont("Arial", 10)
    else:
        roi_btn_font = QFont("Arial", 10.5, QFont.Bold)

    return roi_btn_font


def statusLabelStyle():
    # Style for status bar
    status_label_style = """QLabel {
                                    color:white;
                                    font-family:Arial;
                                    font-style:italic;
                                    font-size:10
                                    }"""
    return status_label_style


def parameterInputStyle():
    # Style for parameter fields
    parameter_input_style = """QLineEdit {
                                          background-color:white;
                                          font-family:Arial;
                                          font-size:8;
                                          }"""
    return parameter_input_style


def parameterLabelStyle():
    # Style for parameter field labels
    parameter_label_style = """QLabel {
                                        color:white;
                                        font-family:Arial;
                                        font-size:8;
                                        }"""
    return parameter_label_style


def parameterLabelFont():
    # Style for parameter fields label fonts
    parameter_label_font = QFont("Arial", 10)
    parameter_label_font.setItalic(True)

    return parameter_label_font


def parameterSubLabelStyle():
    # Style for text below parameter input fields
    parameter_sub_label_style = """QLabel {
                                           color:grey;
                                           font-family:Arial;
                                           font-size:8;
                                           }"""
    return parameter_sub_label_style


def parameterSubLabelFont():
    # Style for parameter sub labels
    parameter_sub_label_font = QFont("Arial", 8)
    parameter_sub_label_font.setItalic(True)

    return parameter_sub_label_font


def sensorInputStyle():
    # Style for the imaging sensor combobox
    sensor_input_style = """QComboBox {
                                        background:white;
                                        }
                            QComboBox QAbstractItemView {
                                                background:white;
                                                        }"""

    return sensor_input_style


def flagInputStyle():
    # Style for the ROI flag input dialog window
    flag_input_style = """QInputDialog {
                                        background:white;
                                        }"""

    return flag_input_style


def parameterCheckBoxStyle():
    # Style for parameter checkboxes
    param_check_style = """QCheckBox {
                                        color:white;
                                        }"""
    return param_check_style


def roiListStyle():
    # Style for roi list frame
    roi_list_style = """QListWidget {
                                    background:black;
                                    border:0px;
                                    }
                        QListWidget::Item:unselected {
                                    background:black;
                                    color:white;
                                    }
                        QListWidget::Item:selected {
                                    background: #02449B;
                                    color:white;
                                    }
                        QListWidget::Item:hover {
                                    background: #132743;
                                    color:white;
                                    }
                                    """
    return roi_list_style
