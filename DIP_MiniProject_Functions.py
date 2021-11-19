import cv2
import pytesseract
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt
from imutils import perspective
from scipy.spatial.distance import euclidean


class Functions:
    # ########################################  PUT TEXT & BOX  ########################################
    @staticmethod
    def draw_shapes(img_contours, img, detection, box_color, box_pixel, text_color, text_pixel):
        if detection == 1:
            pytesseract.pytesseract.tesseract_cmd = r'pic\tesseract.exe'
            h_img, w_img, _ = img.shape
            boxes = pytesseract.image_to_boxes(img)
            lower_alphabet = [str('a'), str('b'), str('c'), str('d'), str('e'), str('f'), str('g'), str('h'), str('i'),
                              str('j'), str('k'), str('l'), str('m'), str('n'), str('o'), str('p'), str('q'), str('r'),
                              str('s'), str('t'), str('u'), str('v'), str('w'), str('x'), str('y'), str('z')]
            upper_alphabet = [str('A'), str('B'), str('C'), str('D'), str('E'), str('F'), str('G'), str('H'), str('I'),
                              str('J'), str('K'), str('L'), str('M'), str('N'), str('O'), str('P'), str('Q'), str('R'),
                              str('S'), str('T'), str('U'), str('V'), str('W'), str('X'), str('Y'), str('Z')]
            number = [str('0'), str('1'), str('2'), str('3'), str('4'), str('5'),
                      str('6'), str('7'), str('8'), str('09')]
            for b in boxes.splitlines():
                b = b.split(' ')
                for i in range(len(b)):
                    for j in range(len(lower_alphabet)):
                        if b[0] == lower_alphabet[j] or b[0] == upper_alphabet[j]:
                            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                            cv2.rectangle(img, (x, h_img - y), (w, h_img - h), box_color, box_pixel)
                            cv2.putText(img, b[0], (x, h_img - y + 15), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, text_color, text_pixel)
                    for j in range(len(number)):
                        if b[0] == number[j]:
                            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                            cv2.rectangle(img, (x, h_img - y), (w, h_img - h), box_color, box_pixel)
                            cv2.putText(img, b[0], (x, h_img - y + 15), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, text_color, text_pixel)
        ref_object = img_contours[0]
        box = cv2.minAreaRect(ref_object)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        dist_in_pixel = euclidean(tl, tr)
        dist_in_cm = 2
        pixel_per_cm = dist_in_pixel / dist_in_cm
        for contour in img_contours:
            box1 = cv2.minAreaRect(contour)
            box1 = cv2.boxPoints(box1)
            box1 = np.array(box1, dtype="int")
            box1 = perspective.order_points(box1)
            if detection == 2:
                box = cv2.minAreaRect(contour)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
                (tl, tr, br, bl) = box
                wid = euclidean(tl, tr) / pixel_per_cm
                ht = euclidean(tr, br) / pixel_per_cm
                area = cv2.contourArea(contour)
                if area > 100:
                    cv2.drawContours(img, [box1.astype("int")], -1, box_color, box_pixel)
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                    x, y, w, h = cv2.boundingRect(approx)
                    cv2.putText(img, '{:.1f}'.format(wid) + 'x' + '{:.1f}'.format(ht), (x, y + h + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, text_pixel)
            if detection == 3:
                box = cv2.minAreaRect(contour)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
                (tl, tr, br, bl) = box
                wid = euclidean(tl, tr) / pixel_per_cm
                ht = euclidean(tr, br) / pixel_per_cm
                area = cv2.contourArea(contour)
                if area > 100:
                    cv2.drawContours(img, [box1.astype("int")], -1, box_color, box_pixel)
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                    x, y, w, h = cv2.boundingRect(approx)
                    if len(approx) == 3:
                        shape = str('Triangle')
                    elif len(approx) == 4:
                        if 0 <= wid - ht <= 0.15 or 0 <= ht - wid <= 0.15:
                            shape = str('Square')
                        else:
                            shape = str('Rectangle')
                    elif len(approx) == 5:
                        shape = str('Pentagon')
                    elif len(approx) == 6:
                        shape = str('Hexagon')
                    elif len(approx) == 7:
                        shape = str('Heptagon')
                    elif len(approx) == 8:
                        shape = str('Octagon')
                    elif len(approx) == 9:
                        shape = str('Nonagon')
                    elif len(approx) == 10:
                        shape = str('Decagon')
                    else:
                        shape = str('Unknown')
                    if y + h + 15 > img.shape[0] or y + h + 35 > img.shape[0]:
                        cv2.putText(img, '{:.1f}'.format(wid) + 'x' + '{:.1f}'.format(ht) + '(cm)', (x, y - 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, text_pixel)
                        cv2.putText(img, str(len(approx)) + 'v, ' + shape, (x, y - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, text_pixel)
                    else:
                        cv2.putText(img, '{:.1f}'.format(wid) + 'x' + '{:.1f}'.format(ht) + '(cm)', (x, y + h + 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, text_pixel)
                        cv2.putText(img, str(len(approx)) + 'v, ' + shape, (x, y + h + 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, text_pixel)

    # ########################################  LABEL  ########################################
    @staticmethod
    def print_canny_threshold_num(technique, l_canny_threshold, canny_threshold_x, canny_threshold_y,
                                  canny_threshold_width, canny_threshold_height, canny_num):
        if technique == 1:
            l_canny_threshold.setGeometry(canny_threshold_x, canny_threshold_y,
                                          canny_threshold_width, canny_threshold_height)
        else:
            l_canny_threshold.setGeometry(canny_threshold_x + 5000, canny_threshold_y + 5000,
                                          canny_threshold_width, canny_threshold_height)
        l_canny_threshold.setText('Threshold:  ' + str(canny_num))
        l_canny_threshold.setFont(QFont('Arial', 9))

    @staticmethod
    def print_default(num, technique, detection, l_default, default_x, default_y, default_width, default_height,
                      box_color, box_pixel, text_color, text_pixel, obj_number):
        if box_color == (0, 0, 255):
            b_color = str('red')
        elif box_color == (0, 255, 0):
            b_color = str('green')
        else:
            b_color = str('blue')
        if text_color == (0, 0, 255):
            t_color = str('red')
        elif text_color == (0, 255, 0):
            t_color = str('green')
        else:
            t_color = str('blue')
        if technique == 1:
            technique = str('Canny')
        elif technique == 2:
            technique = str('Prewitt')
        else:
            technique = str('Sobel')
        if detection == 1 or detection == 2:
            detector = str('Character')
        else:
            detector = str('Shape')
        if num == 1:
            l_default.setText('   Properties :  Box - ' + b_color + ', ' +
                              str(box_pixel) + 'px   ;   Text - ' + t_color + ', ' +
                              str(text_pixel) + 'px   ;   Technique - ' + technique +
                              '   ;   Detector - ' + detector)
        elif num == 2:
            l_default.setText('   Properties :  Box - ' + b_color + ', ' +
                              str(box_pixel) + 'px   ;   Text - ' + t_color + ', ' +
                              str(text_pixel) + 'px   ;   Technique - ' + technique +
                              '   ;   Detector - ' + detector +
                              '   ;   Number of Detected Object - ' + str(obj_number))
        l_default.setGeometry(default_x, default_y, default_width, default_height)
        l_default.setFont(QFont('Arial', 9))
        l_default.setStyleSheet("background-color: darkgray")

    @staticmethod
    def print_image(image, num, detect_button, l_ori_image, l_detected_image, width_scale, height_scale,
                    frame1_x, frame1_y, frame1_width, frame1_height, frame2_x, frame2_y, frame2_width, frame2_height,
                    bg_x, bg_y):
        detect_button.setEnabled(True)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        qformat = QImage.Format_ARGB32
        img = QImage(image.data, int(image.shape[1]), int(image.shape[0]), int(qformat))
        if num == 1:
            l_ori_image.setPixmap((QPixmap.scaled(QPixmap.fromImage(img), int(image.shape[1] * width_scale),
                                                  int(image.shape[0] * height_scale), Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation)))
            l_ori_image.setGeometry(int(((frame1_width + (bg_x * 3) + frame1_x) - (image.shape[1] * width_scale))/2),
                                    int(((frame1_height + (bg_y * 3) + frame1_y) - (image.shape[0] * height_scale))/2),
                                    int(image.shape[1] * width_scale), int(image.shape[0] * height_scale))
        elif num == 2:
            l_detected_image.setPixmap((QPixmap.scaled(QPixmap.fromImage(img), int(image.shape[1] * width_scale),
                                                       int(image.shape[0] * height_scale), Qt.KeepAspectRatio,
                                                       Qt.SmoothTransformation)))
            l_detected_image.setGeometry(int(((frame2_width + (bg_x * 42) + frame2_x)
                                              - (image.shape[1] * width_scale)) / 2),
                                         int(((frame2_height + (bg_y * 3) + frame2_y)
                                              - (image.shape[0] * height_scale)) / 2),
                                         int(image.shape[1] * width_scale), int(image.shape[0] * height_scale))
