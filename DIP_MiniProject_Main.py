import sys
import cv2
import imutils
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QLabel, QPushButton, QDesktopWidget,\
    QFileDialog, QFrame, QSlider, QDialog, QGroupBox, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from imutils import contours
from skimage.util import img_as_ubyte
from skimage.morphology import skeletonize, thin
from DIP_MiniProject_GUI import GUI
from DIP_MIniProject_ExtraWin import InstructionWindow, AboutWindow
from DIP_MiniProject_Functions import Functions


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        # window
        self.title = 'DIP Mini Project'
        self.win_width = 1200
        self.win_height = 750
        # background label
        self.bg_x = 15
        self.bg_y = 35
        self.bg_width = 1170
        self.bg_height = 670
        # properties label
        self.default_x = 0
        self.default_y = 713
        self.default_width = 1200
        self.default_height = 37
        self.obj_number = 0
        # text label
        self.text1_x = 250
        self.text1_y = 45
        self.text1_width = 150
        self.text1_height = 37
        self.text2_x = 835
        self.text2_y = 45
        self.text2_width = 150
        self.text2_height = 37
        # canny threshold label
        self.canny_threshold_x = 865
        self.canny_threshold_y = 716
        self.canny_threshold_width = 120
        self.canny_threshold_height = 30
        # frames
        self.frame1_x = 20
        self.frame1_y = 45
        self.frame1_width = 550
        self.frame1_height = 550
        self.frame2_x = 600
        self.frame2_y = 45
        self.frame2_width = 550
        self.frame2_height = 550
        # button
        self.detect_button_y = 645
        self.detect_button_width = 120
        self.detect_button_height = 50
        self.button_width = 55
        self.button_height = 55
        self.edge_button_x = 1120
        self.edge_button_y = 640
        self.phone_button_x = 1055
        self.phone_button_y = 640
        self.camera_button_x = 990
        self.camera_button_y = 640
        # slider
        self.slider_x = 980
        self.slider_y = 717
        self.slider_width = 200
        self.slider_height = 30
        self.canny_num = 50
        # maximum image dimension
        self.max_img_width = 500
        self.max_img_height = 500
        # box, text
        self.box_color = (255, 0, 0)
        self.text_color = (0, 0, 255)
        self.box_pixel = 1
        self.text_pixel = 1
        # technique
        self.technique = 1
        self.canny = True
        self.prewitt = False
        self.sobel = False
        # detector
        self.detection = 3
        # image
        self.width_scale = 1
        self.height_scale = 1
        self.filename = None
        self.original_image = None
        self.detected_image = None
        self.instant_image = None
        self.detected = False
        # class
        self.gui = GUI()
        self.functions = Functions()
        self.instruction_window = InstructionWindow()
        self.about_window = AboutWindow()
        # declare gui
        self.l_background = QLabel(self)
        self.l_default = QLabel(self)
        self.l_ori_image = QLabel(self)
        self.l_detected_image = QLabel(self)
        self.l_text1 = QLabel(self)
        self.l_text2 = QLabel(self)
        self.l_canny_threshold = QLabel(self)
        self.frame1 = QFrame(self.l_background)
        self.frame2 = QFrame(self.l_background)
        self.detect_button = QPushButton('DETECT', self)
        self.edge_button = QPushButton('', self)
        self.camera_button = QPushButton('', self)
        self.phone_button = QPushButton('', self)
        self.canny_slider = QSlider(Qt.Horizontal, self)
        self.dialog = QDialog(self)
        self.form_group_box = QGroupBox('Insert Your Phone IP Address')
        self.text_box = QLineEdit(self)
        self.m_file = self.menuBar().addMenu('File')
        self.m_edit = self.menuBar().addMenu('Edit')
        self.m_technique = self.menuBar().addMenu('Technique')
        self.m_detector = self.menuBar().addMenu('Detector')
        self.m_help = self.menuBar().addMenu('Help')
        # <<<<<<<<<<<<<<<<<<<<<<<<<  In File  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.a_open = QAction('Open', self)
        self.a_open.setIcon(QIcon(r'pic\icon\icon_open.png'))
        self.a_save = QAction('Save', self)
        self.a_save.setIcon(QIcon(r'pic\icon\icon_save.png'))
        self.a_exit = QAction('Exit', self)
        self.a_exit.setIcon(QIcon(r'pic\icon\icon_exit.png'))
        # <<<<<<<<<<<<<<<<<<<<<<<<<  In Edit  >>>>>>>>>>>>>>>>>>>>>>>>>
        # ***************  Add Menu  ***************
        self.a_box = self.m_edit.addMenu('Box')
        self.a_box.setIcon(QIcon(r'pic\icon\icon_box.png'))
        self.a_text = self.m_edit.addMenu('Text')
        self.a_text.setIcon(QIcon(r'pic\icon\icon_text.png'))
        self.a_box_color = self.a_box.addMenu('Color')
        self.a_box_color.setIcon(QIcon(r'pic\icon\icon_color.png'))
        self.a_box_pixel = self.a_box.addMenu('Pixel')
        self.a_box_pixel.setIcon(QIcon(r'pic\icon\icon_pixel.png'))
        self.a_text_color = self.a_text.addMenu('Color')
        self.a_text_color.setIcon(QIcon(r'pic\icon\icon_color.png'))
        self.a_text_pixel = self.a_text.addMenu('Pixel')
        self.a_text_pixel.setIcon(QIcon(r'pic\icon\icon_pixel.png'))
        # ***************  Color  ***************
        self.a_box_color_blue = QAction('Blue', self)
        self.a_box_color_blue.setIcon(QIcon(r'pic\icon\icon_blue.png'))
        self.a_box_color_green = QAction('Green', self)
        self.a_box_color_green.setIcon(QIcon(r'pic\icon\icon_green.png'))
        self.a_box_color_red = QAction('Red', self)
        self.a_box_color_red.setIcon(QIcon(r'pic\icon\icon_red.png'))
        self.a_text_color_blue = QAction('Blue', self)
        self.a_text_color_blue.setIcon(QIcon(r'pic\icon\icon_blue.png'))
        self.a_text_color_green = QAction('Green', self)
        self.a_text_color_green.setIcon(QIcon(r'pic\icon\icon_green.png'))
        self.a_text_color_red = QAction('Red', self)
        self.a_text_color_red.setIcon(QIcon(r'pic\icon\icon_red.png'))
        # ***************  Pixel  ***************
        self.a_box_pixel_1 = QAction('1', self)
        self.a_box_pixel_2 = QAction('2', self)
        self.a_text_pixel_1 = QAction('1', self)
        self.a_text_pixel_2 = QAction('2', self)
        # <<<<<<<<<<<<<<<<<<<<<<<<<  In Technique  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.a_canny = QAction('Canny', self)
        self.a_sobel = QAction('Sobel', self)
        self.a_prewitt = QAction('Prewitt', self)
        # <<<<<<<<<<<<<<<<<<<<<<<<<  In Detector  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.a_shape = QAction('Shape', self)
        self.a_character = self.m_detector.addMenu('Character')
        self.a_character_chr = QAction('Character', self)
        self.a_character_size = QAction('Size', self)
        # <<<<<<<<<<<<<<<<<<<<<<<<<  In Help  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.a_instruction = QAction('Instruction', self)
        self.a_instruction.setIcon(QIcon(r'pic\icon\icon_instruction.png'))
        self.a_about = QAction('About', self)
        self.a_about.setIcon(QIcon(r'pic\icon\icon_about.png'))

        self.init_ui()

    def init_ui(self):
        self.resize(self.win_width, self.win_height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_win.png'))
        self.move_window()
        self.gui.background(self.l_background, self.bg_x, self.bg_y, self.bg_width, self.bg_height, self.l_text1,
                            self.text1_x, self.text1_y, self.text1_width, self.text1_height, self.l_text2,
                            self.text2_x, self.text2_y, self.text2_width, self.text2_height)
        self.gui.frame(self.frame1, self.frame1_x, self.frame1_y, self.frame1_width, self.frame1_height,
                       self.frame2, self.frame2_x, self.frame2_y, self.frame2_width, self.frame2_height)
        self.gui.button(self.bg_x, self.bg_width, self.detect_button, self.detect_button_y, self.detect_button_width,
                        self.detect_button_height, self.button_width, self.button_height, self.edge_button,
                        self.edge_button_x, self.edge_button_y, self.phone_button, self.phone_button_x,
                        self.phone_button_y, self.camera_button, self.camera_button_x, self.camera_button_y,
                        self.detect_upload_image, self.show_edge_detection, self.open_dialog, self.pc_detect_real_time)
        self.functions.print_canny_threshold_num(self.technique, self.l_canny_threshold, self.canny_threshold_x,
                                                 self.canny_threshold_y, self.canny_threshold_width, 
                                                 self.canny_threshold_height, self.canny_num)
        self.gui.slider(self.technique, self.canny_slider, self.slider_x, self.slider_y, self.slider_width,
                        self.slider_height, self.canny_num, self.change_canny_num)
        self.menu_bar()
        self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                     self.default_y, self.default_width, self.default_height, self.box_color,
                                     self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        self.show()
        self.gui.ip_address_dialog(self.dialog, self.form_group_box, self.text_box,
                                   self.phone_detect_real_time, self.close_dialog)

    def move_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # ########################################  MENU BAR  ########################################
    def menu_bar(self):
        # <<<<<<<<<<<<<<<<<<<<<<<<<  File  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.a_open.setShortcut('Ctrl+O')
        self.a_open.triggered.connect(self.browse_image)
        self.a_save.setShortcut('Ctrl+S')
        self.a_save.triggered.connect(self.save_image)
        self.a_save.setEnabled(False)
        self.a_exit.setShortcut('Ctrl+E')
        self.a_exit.triggered.connect(self.close_window)
        self.m_file.addAction(self.a_open)
        self.m_file.addSeparator()
        self.m_file.addAction(self.a_save)
        self.m_file.addSeparator()
        self.m_file.addAction(self.a_exit)
        # <<<<<<<<<<<<<<<<<<<<<<<<<  Edit  >>>>>>>>>>>>>>>>>>>>>>>>>
        # ***************  Box Color  ***************
        self.a_box_color.addAction(self.a_box_color_blue)
        self.a_box_color_blue.triggered.connect(self.set_box_blue)
        self.a_box_color.addSeparator()
        self.a_box_color.addAction(self.a_box_color_green)
        self.a_box_color_green.triggered.connect(self.set_box_green)
        self.a_box_color.addSeparator()
        self.a_box_color.addAction(self.a_box_color_red)
        self.a_box_color_red.triggered.connect(self.set_box_red)
        # ***************  Text Color  ***************
        self.a_text_color.addAction(self.a_text_color_blue)
        self.a_text_color_blue.triggered.connect(self.set_text_blue)
        self.a_text_color.addSeparator()
        self.a_text_color.addAction(self.a_text_color_green)
        self.a_text_color_green.triggered.connect(self.set_text_green)
        self.a_text_color.addSeparator()
        self.a_text_color.addAction(self.a_text_color_red)
        self.a_text_color_red.triggered.connect(self.set_text_red)
        # ***************  Box Pixel  ***************
        self.a_box_pixel.addAction(self.a_box_pixel_1)
        self.a_box_pixel_1.setCheckable(True)
        self.a_box_pixel_1.setChecked(True)
        self.a_box_pixel_1.triggered.connect(self.set_box_pixel_1)
        self.a_box_pixel.addSeparator()
        self.a_box_pixel.addAction(self.a_box_pixel_2)
        self.a_box_pixel_2.setCheckable(True)
        self.a_box_pixel_2.triggered.connect(self.set_box_pixel_2)
        # ***************  Text Pixel  ***************
        self.a_text_pixel.addAction(self.a_text_pixel_1)
        self.a_text_pixel_1.setCheckable(True)
        self.a_text_pixel_1.setChecked(True)
        self.a_text_pixel_1.triggered.connect(self.set_text_pixel_1)
        self.a_text_pixel.addSeparator()
        self.a_text_pixel.addAction(self.a_text_pixel_2)
        self.a_text_pixel_2.triggered.connect(self.set_text_pixel_2)
        self.a_text_pixel_2.setCheckable(True)
        # <<<<<<<<<<<<<<<<<<<<<<<<<  Technique  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.m_technique.addAction(self.a_canny)
        self.a_canny.setCheckable(True)
        self.a_canny.setChecked(True)
        self.a_canny.triggered.connect(self.canny_operation)
        self.m_technique.addSeparator()
        self.m_technique.addAction(self.a_prewitt)
        self.a_prewitt.setCheckable(True)
        self.a_prewitt.triggered.connect(self.prewitt_operation)
        self.m_technique.addSeparator()
        self.m_technique.addAction(self.a_sobel)
        self.a_sobel.setCheckable(True)
        self.a_sobel.triggered.connect(self.sobel_operation)
        # <<<<<<<<<<<<<<<<<<<<<<<<<  Detector  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.a_character.addAction(self.a_character_chr)
        self.a_character_chr.setCheckable(True)
        self.a_character_chr.triggered.connect(self.character_chr)
        self.a_character.addSeparator()
        self.a_character.addAction(self.a_character_size)
        self.a_character_size.setCheckable(True)
        self.a_character_size.triggered.connect(self.character_size)
        self.m_detector.addSeparator()
        self.m_detector.addAction(self.a_shape)
        self.a_shape.setCheckable(True)
        self.a_shape.setChecked(True)
        self.a_shape.triggered.connect(self.shape_operation)
        # <<<<<<<<<<<<<<<<<<<<<<<<<  Help  >>>>>>>>>>>>>>>>>>>>>>>>>
        self.a_instruction.setShortcut('Ctrl+I')
        self.a_instruction.triggered.connect(self.open_instruction_window)
        self.a_about.triggered.connect(self.open_about_window)
        self.m_help.addAction(self.a_instruction)
        self.m_help.addSeparator()
        self.m_help.addAction(self.a_about)

    # ########################################  FILE  ########################################
    def browse_image(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '.', 'Image Files (*.png *.jpg *.jpeg)')
        if self.filename:
            self.original_image = cv2.imread(self.filename, 1)
            self.detected_image = cv2.imread(self.filename, 1)
            self.height_scale = 1
            self.width_scale = 1
            self.l_detected_image.move(5000, 5000)
            self.detected = False
            if self.original_image.shape[1] > self.max_img_width:
                img_w = self.original_image.shape[1] / self.original_image.shape[1] * self.max_img_width
                self.width_scale = img_w / self.original_image.shape[1]
                self.height_scale = self.width_scale
                if self.original_image.shape[0] * self.height_scale > self.max_img_height:
                    img_h = self.original_image.shape[0] / self.original_image.shape[0] * self.max_img_height
                    self.height_scale = img_h / self.original_image.shape[0]
                    self.width_scale = self.height_scale
            elif self.original_image.shape[0] > self.max_img_height:
                img_h = self.original_image.shape[0] / self.original_image.shape[0] * self.max_img_height
                self.height_scale = img_h / self.original_image.shape[0]
                self.width_scale = self.height_scale
                if self.original_image.shape[1] * self.width_scale > self.max_img_width:
                    img_w = self.original_image.shape[1] / self.original_image.shape[1] * self.max_img_width
                    self.width_scale = img_w / self.original_image.shape[1]
                    self.height_scale = self.width_scale
            self.functions.print_image(self.original_image, 1, self.detect_button, self.l_ori_image,
                                       self.l_detected_image, self.width_scale, self.height_scale, self.frame1_x,
                                       self.frame1_y, self.frame1_width, self.frame1_height, self.frame2_x,
                                       self.frame2_y, self.frame2_width, self.frame2_height, self.bg_x, self.bg_y)

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                   "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if file_path:
            cv2.imwrite(file_path, self.detected_image)

    def close_window(self):
        self.close()

    # ########################################  EDIT  ########################################
    def set_box_blue(self):
        self.box_color = (255, 0, 0)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_box_green(self):
        self.box_color = (0, 255, 0)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_box_red(self):
        self.box_color = (0, 0, 255)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_text_blue(self):
        self.text_color = (255, 0, 0)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_text_green(self):
        self.text_color = (0, 255, 0)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_text_red(self):
        self.text_color = (0, 0, 255)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_box_pixel_1(self):
        self.a_box_pixel_1.setChecked(True)
        self.a_box_pixel_2.setChecked(False)
        self.box_pixel = 1
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_box_pixel_2(self):
        self.a_box_pixel_1.setChecked(False)
        self.a_box_pixel_2.setChecked(True)
        self.box_pixel = 2
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_text_pixel_1(self):
        self.a_text_pixel_1.setChecked(True)
        self.a_text_pixel_2.setChecked(False)
        self.text_pixel = 1
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def set_text_pixel_2(self):
        self.a_text_pixel_1.setChecked(False)
        self.a_text_pixel_2.setChecked(True)
        self.text_pixel = 2
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    # ########################################  TECHNIQUE  ########################################
    def canny_operation(self):
        self.technique = 1
        self.canny = True
        self.prewitt = False
        self.sobel = False
        self.a_canny.setChecked(True)
        self.a_prewitt.setChecked(False)
        self.a_sobel.setChecked(False)
        self.functions.print_canny_threshold_num(self.technique, self.l_canny_threshold, self.canny_threshold_x,
                                                 self.canny_threshold_y, self.canny_threshold_width,
                                                 self.canny_threshold_height, self.canny_num)
        self.gui.slider(self.technique, self.canny_slider, self.slider_x, self.slider_y, self.slider_width,
                        self.slider_height, self.canny_num, self.change_canny_num)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def prewitt_operation(self):
        self.technique = 2
        self.canny = False
        self.prewitt = True
        self.sobel = False
        self.a_canny.setChecked(False)
        self.a_prewitt.setChecked(True)
        self.a_sobel.setChecked(False)
        self.functions.print_canny_threshold_num(self.technique, self.l_canny_threshold, self.canny_threshold_x,
                                                 self.canny_threshold_y, self.canny_threshold_width,
                                                 self.canny_threshold_height, self.canny_num)
        self.gui.slider(self.technique, self.canny_slider, self.slider_x, self.slider_y, self.slider_width,
                        self.slider_height, self.canny_num, self.change_canny_num)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def sobel_operation(self):
        self.technique = 3
        self.canny = False
        self.prewitt = False
        self.sobel = True
        self.a_canny.setChecked(False)
        self.a_prewitt.setChecked(False)
        self.a_sobel.setChecked(True)
        self.functions.print_canny_threshold_num(self.technique, self.l_canny_threshold, self.canny_threshold_x,
                                                 self.canny_threshold_y, self.canny_threshold_width,
                                                 self.canny_threshold_height, self.canny_num)
        self.gui.slider(self.technique, self.canny_slider, self.slider_x, self.slider_y, self.slider_width,
                        self.slider_height, self.canny_num, self.change_canny_num)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    # ########################################  DETECTOR  ########################################
    def character_chr(self):
        self.detection = 1
        self.a_shape.setChecked(False)
        self.a_character_chr.setChecked(True)
        self.a_character_size.setChecked(False)
        self.character_operation()

    def character_size(self):
        self.detection = 2
        self.a_shape.setChecked(False)
        self.a_character_chr.setChecked(False)
        self.a_character_size.setChecked(True)
        self.character_operation()

    def character_operation(self):
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def shape_operation(self):
        self.detection = 3
        self.a_shape.setChecked(True)
        self.a_character_chr.setChecked(False)
        self.a_character_size.setChecked(False)
        if self.detected:
            self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)
        else:
            self.functions.print_default(1, self.technique, self.detection, self.l_default, self.default_x,
                                         self.default_y, self.default_width, self.default_height, self.box_color,
                                         self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    # ########################################  HELP  ########################################
    def open_instruction_window(self):
        self.instruction_window.show()

    def open_about_window(self):
        self.about_window.show()

    # ########################################  DETECT PROCESS  ########################################
    def change_canny_num(self, x):
        self.canny_num = x
        self.functions.print_canny_threshold_num(self.technique, self.l_canny_threshold, self.canny_threshold_x,
                                                 self.canny_threshold_y, self.canny_threshold_width,
                                                 self.canny_threshold_height, self.canny_num)

    def open_dialog(self):
        self.text_box.clear()
        self.dialog.show()

    def close_dialog(self):
        self.dialog.close()

    def detect_upload_image(self):
        self.edge_button.setEnabled(True)
        self.a_save.setEnabled(True)
        self.instant_image = None
        self.original_image = cv2.imread(self.filename, 1)
        self.detected_image = cv2.imread(self.filename, 1)
        self.detect_technique(self.original_image)
        img_contours = cv2.findContours(self.instant_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_contours = imutils.grab_contours(img_contours)
        (img_contours, _) = contours.sort_contours(img_contours)
        img_contours = [x for x in img_contours if cv2.contourArea(x) > 100]
        self.functions.draw_shapes(img_contours, self.detected_image, self.detection, self.box_color, self.box_pixel,
                                   self.text_color, self.text_pixel)
        self.obj_number = len(img_contours)
        for i, img in enumerate([self.detected_image]):
            self.functions.print_image(img, 2, self.detect_button, self.l_ori_image, self.l_detected_image,
                                       self.width_scale, self.height_scale, self.frame1_x, self.frame1_y,
                                       self.frame1_width, self.frame1_height, self.frame2_x, self.frame2_y,
                                       self.frame2_width, self.frame2_height, self.bg_x, self.bg_y)
        self.detected = True
        self.functions.print_default(2, self.technique, self.detection, self.l_default, self.default_x,
                                     self.default_y, self.default_width, self.default_height, self.box_color,
                                     self.box_pixel, self.text_color, self.text_pixel, self.obj_number)

    def pc_detect_real_time(self):
        video = cv2.VideoCapture(0)
        video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.instant_image = None
        while True:
            success, img = video.read()
            self.detect_technique(img)
            img_contours = cv2.findContours(self.instant_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            img_contours = imutils.grab_contours(img_contours)
            (img_contours, _) = contours.sort_contours(img_contours)
            img_contours = [x for x in img_contours if cv2.contourArea(x) > 100]
            if len(img_contours) != 0:
                self.functions.draw_shapes(img_contours, img, self.detection, self.box_color, self.box_pixel,
                                           self.text_color, self.text_pixel)
            cv2.imshow('PC Camera', img)
            cv2.moveWindow('PC Camera', 310, 150)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()

    def phone_detect_real_time(self):
        self.dialog.close()
        self.instant_image = None
        ip_address = self.text_box.text() + str('/video')
        video = cv2.VideoCapture(0)
        video.open(ip_address)
        while True:
            success, img = video.read()
            img = imutils.resize(img, 1280, 720)
            self.detect_technique(img)
            img_contours = cv2.findContours(self.instant_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            img_contours = imutils.grab_contours(img_contours)
            (img_contours, _) = contours.sort_contours(img_contours)
            img_contours = [x for x in img_contours if cv2.contourArea(x) > 100]
            if len(img_contours) != 0:
                self.functions.draw_shapes(img_contours, img, self.detection, self.box_color, self.box_pixel,
                                           self.text_color, self.text_pixel)
            cv2.imshow('Phone Camera', img)
            cv2.moveWindow('Phone Camera', 310, 150)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()

    def thinning(self):
        self.threshold()
        skeleton = skeletonize(self.instant_image)
        self.instant_image = img_as_ubyte(skeleton)
        self.instant_image = cv2.dilate(self.instant_image, None, iterations=1)
        self.instant_image = cv2.erode(self.instant_image, None, iterations=1)
        self.threshold()
        self.instant_image = thin(self.instant_image)
        self.instant_image = img_as_ubyte(self.instant_image)

    def threshold(self):
        if self.canny:
            _, self.instant_image = cv2.threshold(self.instant_image, 10, 1, cv2.THRESH_BINARY)
        elif self.prewitt:
            _, self.instant_image = cv2.threshold(self.instant_image, 30, 1, cv2.THRESH_BINARY)
        else:
            _, self.instant_image = cv2.threshold(self.instant_image, 100, 1, cv2.THRESH_BINARY)

    def detect_technique(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        if self.canny:
            self.instant_image = cv2.Canny(blur, self.canny_num, 255)
            self.thinning()
        elif self.prewitt:
            kernel_x = np.array([[-1, 0, 1],
                                 [-1, 0, 1],
                                 [-1, 0, 1]])
            kernel_y = np.array([[1, 1, 1],
                                 [0, 0, 0],
                                 [-1, -1, -1]])
            gray_x = cv2.filter2D(blur, -1, kernel_x)
            gray_y = cv2.filter2D(blur, -1, kernel_y)
            self.instant_image = cv2.bitwise_or(gray_x, gray_y)
            self.thinning()
        elif self.sobel:
            sobel_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0)
            sobel_x = np.uint8(np.absolute(sobel_x))
            sobel_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1)
            sobel_y = np.uint8(np.absolute(sobel_y))
            self.instant_image = cv2.bitwise_or(sobel_x, sobel_y)
            self.thinning()

    def show_edge_detection(self):
        if self.canny:
            cv2.imshow('Canny', self.instant_image)
            cv2.moveWindow('Canny', int(self.win_width / 2)+65, int(self.win_height / 2)-70)
        elif self.prewitt:
            cv2.imshow('Prewitt', self.instant_image)
            cv2.moveWindow('Prewitt', int(self.win_width / 2)+65, int(self.win_height / 2)-70)
        elif self.sobel:
            cv2.imshow('Sobel', self.instant_image)
            cv2.moveWindow('Sobel', int(self.win_width / 2)+65, int(self.win_height / 2)-70)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
