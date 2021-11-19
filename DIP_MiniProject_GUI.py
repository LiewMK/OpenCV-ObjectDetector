from PyQt5.QtWidgets import QLabel, QFrame, QFormLayout, QDialogButtonBox, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize


class GUI:
    @staticmethod
    def background(l_background, bg_x, bg_y, bg_width, bg_height, l_text1, text1_x, text1_y, text1_width, text1_height,
                   l_text2, text2_x, text2_y, text2_width, text2_height):
        l_background.setGeometry(bg_x, bg_y, bg_width, bg_height)
        l_background.setStyleSheet("background-color: lightgray; border: 1px solid black")
        l_text1.setText('Original Image')
        l_text2.setText('Detected Image')
        l_text1.setGeometry(text1_x, text1_y, text1_width, text1_height)
        l_text2.setGeometry(text2_x, text2_y, text2_width, text2_height)
        l_text1.setFont(QFont('Arial', 10))
        l_text2.setFont(QFont('Arial', 10))

    @staticmethod
    def frame(frame1, frame1_x, frame1_y, frame1_width, frame1_height,
              frame2, frame2_x, frame2_y, frame2_width, frame2_height):
        frame1.setFrameShape(QFrame.StyledPanel)
        frame2.setFrameShape(QFrame.StyledPanel)
        frame1.setGeometry(frame1_x, frame1_y, frame1_width, frame1_height)
        frame2.setGeometry(frame2_x, frame2_y, frame2_width, frame2_height)

    @staticmethod
    def slider(technique, canny_slider, slider_x, slider_y, slider_width, slider_height, canny_num, change_canny_num):
        if technique == 1:
            canny_slider.setGeometry(slider_x, slider_y, slider_width, slider_height)
        else:
            canny_slider.setGeometry(slider_x + 5000, slider_y + 5000, slider_width, slider_height)
        canny_slider.setMaximum(150)
        canny_slider.setMinimum(0)
        canny_slider.setValue(canny_num)
        canny_slider.valueChanged.connect(change_canny_num)

    @staticmethod
    def button(bg_x, bg_width, detect_button, detect_button_y, detect_button_width, detect_button_height, button_width,
               button_height, edge_button, edge_button_x, edge_button_y, phone_button, phone_button_x, phone_button_y,
               camera_button, camera_button_x, camera_button_y, detect_upload_image, show_edge_detection,
               open_dialog, pc_detect_real_time):
        detect_button.setFont(QFont('Arial', 12))
        detect_button.setGeometry(int(((bg_width + (bg_x * 2)) - detect_button_width) / 2),
                                  detect_button_y, detect_button_width, detect_button_height)
        detect_button.clicked.connect(detect_upload_image)
        detect_button.setEnabled(False)
        edge_button.setIcon(QIcon(r'pic\icon\icon_edge.png'))
        edge_button.setIconSize(QSize(40, 40))
        edge_button.setGeometry(edge_button_x, edge_button_y, button_width, button_height)
        edge_button.clicked.connect(show_edge_detection)
        edge_button.setEnabled(False)
        phone_button.setIcon(QIcon(r'pic\icon\icon_phone.png'))
        phone_button.setIconSize(QSize(40, 40))
        phone_button.setGeometry(phone_button_x, phone_button_y, button_width, button_height)
        phone_button.clicked.connect(open_dialog)
        camera_button.setIcon(QIcon(r'pic\icon\icon_camera.png'))
        camera_button.setIconSize(QSize(35, 35))
        camera_button.setGeometry(camera_button_x, camera_button_y, button_width, button_height)
        camera_button.clicked.connect(pc_detect_real_time)

    @staticmethod
    def ip_address_dialog(dialog, form_group_box, text_box, phone_detect_real_time, close_dialog):
        layout = QFormLayout()
        layout.addRow(QLabel("IP Address:"), text_box)
        form_group_box.setLayout(layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(phone_detect_real_time)
        button_box.rejected.connect(close_dialog)
        main_layout = QVBoxLayout()
        main_layout.addWidget(form_group_box)
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        dialog.setWindowTitle('Phone IP Address')
