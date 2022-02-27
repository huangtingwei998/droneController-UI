#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from datetime import datetime

import cv2
import qdarkstyle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os
import os.path

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (960, 720))


class opencamera(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(opencamera, self).__init__(parent)
        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.save = 0
        self.stopsave = 0
        self.pulse=0
    def set_ui(self):

        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()

        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_save_camera = QtWidgets.QPushButton(u'保存视频')
        self.button_close = QtWidgets.QPushButton(u'退出')
        self.button = QtWidgets.QPushButton(u'按键')
        # Button 的颜色修改
        button_color = [self.button_open_camera, self.button_close, self.button_save_camera,self.button]
        for i in range(4):
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                          "QPushButton:hover{color:red}"
                                          "QPushButton{background-color:rgb(78,255,255)}"
                                          "QPushButton{border:2px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}")

        self.button_open_camera.setMinimumHeight(50)
        self.button_save_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)
        self.button.setMinimumHeight(50)
        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()

        self.label_show_camera.setFixedSize(960, 720)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_save_camera)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.button)


        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)

        self.setLayout(self.__layout_main)

        self.setWindowTitle(u'摄像头')
        self.show()

    def setPic(self,px):
        self.label_show_camera.setPixmap(px)

    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.button_save_camera.clicked.connect(self.save)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)
        self.button.clicked.connect(self.pulse1)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)

                self.button_open_camera.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')

    def show_camera(self):
        flag, self.image = self.capread()

        show = cv2.resize(self.image, (960, 720))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)

        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

        if self.save == 1:
            out.write(self.image)

    def show_camera1(self,image):
        show = cv2.resize(image, (960, 540))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))


    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"关闭", u"是否关闭！")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cacel.setText(u'取消')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            #             self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if out.isOpened():
                out.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()

    def save(self):
        self.save = 1

    def capread(self):
        flag, self.image = self.cap.read()
        return flag, self.image
    def pulse1(self):
        self.pulse = self.pulse+1
        print(self.pulse)
        return self.pulse
if __name__ == "__main__":
    App = QApplication(sys.argv)
    App.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = opencamera()
    sys.exit(App.exec_())
