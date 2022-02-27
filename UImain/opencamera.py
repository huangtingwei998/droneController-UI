#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ctypes
import json
import sys
import cv2
import qdarkstyle
import win32con
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import *
from win32process import SuspendThread, ResumeThread
from tracker_main import trackermain
trackermain = trackermain()
from detector_tracker.tracker import *
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (960, 720))


class Worker(QThread):

    valueChanged = pyqtSignal(int)  # 值变化信号
    handle = -1

    def run(self):
        try:
            # 这个目前我没弄明白这里写法
            self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
                win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
        except Exception as e:
            print('get thread handle failed', e)
        print('thread id', int(QThread.currentThreadId()))
        # 循环发送信号
        trackermain.main()


class opencamera(QWidget):
    def __init__(self, parent=None):
        super(opencamera, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()

        timer = QTimer(self)
        timer.timeout.connect(self.text_browser_show)
        timer.start(1000)

        timer2 = QTimer(self)
        timer2.timeout.connect(self.label_show_camera_show)
        timer2.start(10)



    def set_ui(self):
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_main = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QHBoxLayout()
        # 第一个设置框，设置目标跟踪检测
        layout = QVBoxLayout(self)
        self.startButton = QPushButton('开启检测', self, clicked=self.onStart)
        layout.addWidget(self.startButton)
        self.suspendButton = QPushButton('暂停检测', self, clicked=self.onSuspendThread, enabled=False)
        layout.addWidget(self.suspendButton)
        self.resumeButton = QPushButton('继续检测', self, clicked=self.onResumeThread, enabled=False)
        layout.addWidget(self.resumeButton)
        self.stopButton = QPushButton('终止检测', self, clicked=self.onStopThread, enabled=False)
        layout.addWidget(self.stopButton)
        self.groupBox = QGroupBox("目标跟踪设置")
        self.groupBox.setLayout(layout)
        self.groupBox.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。

        layout1 = QVBoxLayout(self)
        self.start = QLabel('请选择类型')
        layout1.addWidget(self.start)
        self.choice = QComboBox()
        self.choice.addItem('1.本机摄像头')
        self.choice.addItem('2.RTSP流')
        self.choice.addItem('3.本地视频')
        self.choice.addItem('4.其他资源')
        self.choice.currentIndexChanged.connect(self.choiceselect)
        layout1.addWidget(self.choice)

        self.isdetect = QLabel('主窗口是否显示原视频->')
        layout1.addWidget(self.isdetect)
        self.isdetectchoice = QComboBox()
        self.isdetectchoice.addItem("是")
        self.isdetectchoice.addItem("否")
        layout1.addWidget(self.isdetectchoice)
        self.groupBox1 = QGroupBox("参数设置")
        self.groupBox1.setLayout(layout1)
        self.groupBox1.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


        # 垂直布局
        layout2 = QVBoxLayout(self)
        self.cameraLabel = QLabel('1.本机摄像头')
        layout2.addWidget(self.cameraLabel)
        self.camerachoice = QComboBox()
        self.camerachoice.addItem("0")
        self.camerachoice.addItem("1")
        layout2.addWidget(self.camerachoice)
        self.rtspLabel = QLabel('2.RTSP流', self)
        layout2.addWidget(self.rtspLabel)
        self.rtsplineedit = QLineEdit()
        self.rtspbuttun = QPushButton('编辑', self)
        layoutrtsp = QHBoxLayout(self)
        layoutrtsp.addWidget(self.rtsplineedit)
        layoutrtsp.addWidget(self.rtspbuttun)
        layout2.addLayout(layoutrtsp)
        self.localtext = QLabel('3.本地视频', self)
        layout2.addWidget(self.localtext)
        self.chociebuttun =  QPushButton('...', self)
        self.chociebuttun.clicked.connect(self.msg)
        self.locallineedit = QLineEdit()
        layoutlocal = QHBoxLayout(self)
        layoutlocal.addWidget(self.locallineedit)
        layoutlocal.addWidget(self.chociebuttun)
        layout2.addLayout(layoutlocal)
        self.othertext = QLabel('4.其他资源', self)
        layout2.addWidget(self.othertext)
        self.otherineedit = QLineEdit()
        layout2.addWidget(self.otherineedit)
        self.groupBox2 = QGroupBox("视频源设置")
        self.groupBox2.setLayout(layout2)
        self.groupBox2.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


        # 默认是本地摄像头，把其他的都关了
        # 把rtsp关闭
        self.rtsplineedit.setEnabled(False)
        self.rtspbuttun.setEnabled(False)
        # 把本地视频关闭
        self.chociebuttun.setEnabled(False)
        self.locallineedit.setEnabled(False)
        # 把其他资源关闭
        self.otherineedit.setEnabled(False)

        self.__layout_fun_button.addWidget(self.groupBox1)
        self.__layout_fun_button.addWidget(self.groupBox2)
        self.finishbuttun = QPushButton("完成")


        # 点击完成按钮，将设置存入json文件中
        self.finishbuttun.clicked.connect(self.finsihjson)

        self.finishbuttun.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.__layout_fun_button.addWidget(self.finishbuttun)
        self.__layout_fun_button.addWidget(self.groupBox)
        self.move(500, 500)

        # 子线程
        self._thread = Worker(self)
        self._thread.finished.connect(self._thread.deleteLater)


        # 主窗口画面
        self.label_show_camera = QtWidgets.QLabel()


        # 结果部分，将其封装到一个QGroupBox("输出结果")里面
        self.datalabel1 = QTextBrowser(self)
        self.datatext = QLabel("日志输出")
        self.datatext.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.datatext.setAlignment(Qt.AlignHCenter)
        self.datalabel2 = QTextBrowser(self)
        self.datatext2 = QLabel("目标当前坐标")
        self.datatext2.setAlignment(Qt.AlignHCenter)
        self.datalayout1 = QVBoxLayout()
        self.datalayout2 = QVBoxLayout()
        self.datalayout1.addWidget(self.datalabel1)
        self.datalayout1.addWidget(self.datatext)
        self.datalayout2.addWidget(self.datalabel2)
        self.datalayout2.addWidget(self.datatext2)
        self.layout3 = QHBoxLayout()
        self.layout3.addLayout(self.datalayout1)
        self.layout3.addLayout(self.datalayout2)
        self.groupBox3 = QGroupBox("输出结果")
        self.groupBox3.setLayout(self.layout3)
        self.groupBox3.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 总体的布局
        self.label_show_camera.setFixedSize(960, 540)
        self.label_show_camera.setAutoFillBackground(False)
        self.__layout_data_show.addLayout(self.__layout_fun_button)
        self.__layout_data_show.addWidget(self.label_show_camera)
        self.__layout_main.addLayout(self.__layout_data_show)
        self.__layout_main.addWidget(self.groupBox3)


        self.setLayout(self.__layout_main)
        # self.label_move.raise_()
        self.setWindowTitle(u'摄像头')


    def msg(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "./",
                                                          "All Files (*);;Mp4 Files (*.mp4)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.locallineedit.setText(fileName)

    def finsihjson(self):
        text = self.choice.currentText()
        if text == '1.本机摄像头':
            choice="1"
            video = self.camerachoice.currentText()
        if text == '2.RTSP流':
            choice = "2"
            video =self.rtsplineedit.text()
        if text == '3.本地视频':
            choice = "3"
            video =self.locallineedit.text()
        if text == '4.其他资源':
            choice = "4"
            video =self.otherineedit.text()
        index = self.isdetectchoice.currentText()
        if index=='是':
            isdetect = '1'
        if index=='否':
            isdetect = '0'

        payload = {
            'choice': choice, "isdetect": isdetect,"video":video
        }
        with open('config/start.json', 'w') as f:
            json.dump(payload, f)


    def choiceselect(self):
        text = self.choice.currentText()
        if text=='1.本机摄像头':
            # 把本地摄像头打开
            self.camerachoice.setEnabled(True)
            # 把rtsp关闭
            self.rtsplineedit.setEnabled(False)
            self.rtspbuttun.setEnabled(False)
            # 把本地视频关闭
            self.chociebuttun.setEnabled(False)
            self.locallineedit.setEnabled(False)
            #把其他资源关闭
            self.otherineedit.setEnabled(False)
        if text=='2.RTSP流':
            # 把本地摄像头打开
            self.camerachoice.setEnabled(False)
            # 把rtsp关闭
            self.rtsplineedit.setEnabled(True)
            self.rtspbuttun.setEnabled(True)
            # 把本地视频关闭
            self.chociebuttun.setEnabled(False)
            self.locallineedit.setEnabled(False)
            #把其他资源关闭
            self.otherineedit.setEnabled(False)
        if text=='3.本地视频':
            # 把本地摄像头打开
            self.camerachoice.setEnabled(False)
            # 把rtsp关闭
            self.rtsplineedit.setEnabled(False)
            self.rtspbuttun.setEnabled(False)
            # 把本地视频关闭
            self.chociebuttun.setEnabled(True)
            self.locallineedit.setEnabled(True)
            #把其他资源关闭
            self.otherineedit.setEnabled(False)
        if text=='4.其他资源':
            # 把本地摄像头打开
            self.camerachoice.setEnabled(False)
            # 把rtsp关闭
            self.rtsplineedit.setEnabled(False)
            self.rtspbuttun.setEnabled(False)
            # 把本地视频关闭
            self.chociebuttun.setEnabled(False)
            self.locallineedit.setEnabled(False)
            #把其他资源关闭
            self.otherineedit.setEnabled(True)


    def onStart(self):
        print('main id', int(QThread.currentThreadId()))
        self._thread.start()  # 启动线程
        self.startButton.setEnabled(False)
        self.suspendButton.setEnabled(True)
        self.stopButton.setEnabled(True)

    def onSuspendThread(self):
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = SuspendThread(self._thread.handle)
        print('挂起线程', self._thread.handle, ret)
        self.suspendButton.setEnabled(False)
        self.resumeButton.setEnabled(True)

    def onResumeThread(self):
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = ResumeThread(self._thread.handle)
        print('恢复线程', self._thread.handle, ret)
        self.suspendButton.setEnabled(True)
        self.resumeButton.setEnabled(False)

    def onStopThread(self):
        self.startButton.setEnabled(False)
        self.suspendButton.setEnabled(False)
        self.resumeButton.setEnabled(False)
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self._thread.handle, 0)
        print('终止线程', self._thread.handle, ret)
        self.stopButton.setEnabled(False)
    # 检测关闭
    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.quit()
        del self._thread
    # 结果输出与目标跟踪坐标的输出
    def text_browser_show(self):
        flag = trackermain.getFLAG()
        if flag==True:
            mes2 =""
            mes = trackermain.getstarnum()
            (c1,c2) = gettrackerpoint()
            self.datalabel1.insertPlainText(mes + '\n')
            my_cursor = self.datalabel1.textCursor()
            self.datalabel1.moveCursor(my_cursor.End)
            if c1==0 and c2==0:
                mes2 = "没有跟踪"
            else:
                mes2 = "目标当前的坐标(" + str(c1) + "," + str(c1) + ")"
                self.datalabel2.insertPlainText(mes2 + '\n')
                my_cursor = self.datalabel2.textCursor()
                self.datalabel2.moveCursor(my_cursor.End)

    # 将检测的画面显示到软件当中
    def label_show_camera_show(self):
        flag = trackermain.getFLAG2()
        if flag==True:
            image = trackermain.getimage()
            show = cv2.resize(image, (960, 540))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

if __name__ == "__main__":
    App = QApplication(sys.argv)
    # App.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = opencamera()
    ex.show()
    sys.exit(App.exec_())
