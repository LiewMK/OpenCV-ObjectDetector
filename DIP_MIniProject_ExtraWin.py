from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtGui import QImage, QBrush, QIcon, QPixmap, QPainter, QPen, QFont, QPalette
from PyQt5.QtCore import QSize, Qt


class InstructionWindow(QWidget):
    def __init__(self, parent=None):
        super(InstructionWindow, self).__init__(parent)
        self.title = 'Instruction'
        self.win_width = 940
        self.win_height = 580
        self.bg_img = QImage(r'pic\win\instruction.jpg')
        self.button = QPushButton('OK', self)
        self.ui_components()

    def ui_components(self):
        self.resize(self.win_width, self.win_height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_instruction.png'))
        self.move_window()
        self.bg()
        self.button.move(827, 540)
        self.button.clicked.connect(self.close_win)

    def bg(self):
        self.bg_img = self.bg_img.scaled(QSize(self.win_width, self.win_height))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(self.bg_img))
        self.setPalette(palette)

    def move_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def close_win(self):
        self.close()


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.title = 'About'
        self.win_width = 600
        self.win_height = 450
        self.label_ums = QLabel(self)
        self.label_mcg = QLabel(self)
        self.label_message01 = QLabel("This product is the mini project for the course \nImage Processing 2020.", self)
        self.label_message02 = QLabel("©2020 Liew Ming Kai BS18110392. All right reserved.", self)
        self.button = QPushButton('OK', self)
        self.ui_components()

    def ui_components(self):
        self.resize(self.win_width, self.win_height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r'pic\icon\icon_about.png'))
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        pixmap = QPixmap(r'pic\logo\UMS_logo.png')
        self.label_ums.setPixmap(pixmap)
        self.label_ums.move(42, 61)
        pixmap = QPixmap(r'pic\logo\MCG_logo.png')
        self.label_mcg.setPixmap(pixmap)
        self.label_mcg.move(350, 54)
        self.label_message01.move(42, 220)
        self.label_message01.setFont(QFont('Arial', 14))
        self.label_message02.move(42, 350)
        self.label_message02.setFont(QFont('Arial', 10))
        self.button.move(485, 405)
        self.button.clicked.connect(self.close_win)

    def move_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def close_win(self):
        self.close()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    @staticmethod
    def draw_line(qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(42, 180, 558, 180)
