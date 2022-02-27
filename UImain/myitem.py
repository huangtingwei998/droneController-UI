import os
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from myitem import *

class Ui_MainWindow(object):
    """
    自动生成的代码, 请不要修改
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 357)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 341, 341))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 10, 81, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

class listWindows2(QMainWindow):
    def __init__(self,listWidget,pushButton):
        super(listWindows2, self).__init__()
        self.listWidget = listWidget
        self.pushButton = pushButton
        self.pushButton.clicked.connect(self.deal)

    def searchimage(self,each_file):
        name = each_file.split("_")
        file_name, ext = os.path.splitext(name)  # 获取到文件的后缀
        all_files = os.listdir("../face_dataset")  # os.curdir 表示当前目录 curdir:currentdirectory
        flag = 0
        for filename in all_files:
            if name == filename:
                flag = 1
                break
        if flag ==1:
            return  "face_dataset/"+filename,file_name
        else:
            return "face_dataset/unknown.JPG","unkown"


    def get_item_wight(self,data,file,each_file):
            # 读取属性
            ship_name = data
            # 总Widget
            wight = QWidget()

            # 总体横向布局
            layout_main = QHBoxLayout()
            # 数据库图片
            map_l = QLabel()  # 头像显示
            map_l.setFixedSize(80, 80)
            maps = QPixmap(file).scaled(80, 80)
            map_l.setPixmap(maps)
            # 采集的图片
            map_l1 = QLabel()  # 头像显示
            map_l1.setFixedSize(80, 80)
            maps1 = QPixmap(each_file).scaled(80, 80)
            map_l1.setPixmap(maps1)
            # 最又的布局

            text = QLabel(str("识别到"+ship_name))

            layout_main.addWidget(map_l)  # 最左边的头像
            layout_main.addWidget(map_l1)
            layout_main.addWidget(text)
            wight.setLayout(layout_main)  # 布局给wight
            return wight  # 返回wight

    def deal(self):
        all_files = os.listdir("../face")  # os.curdir 表示当前目录 curdir:currentdirectory
        for each_file in all_files:
            image,filename = self.searchimage(each_file)
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(200, 80))  # 设置QListWidgetItem大小
            widget = self.get_item_wight(filename,image,"face/"+each_file)  # 调用上面的函数获取对应data,file,each_file
            self.listWidget.addItem(item)  # 添加item
            self.listWidget.setItemWidget(item, widget)  # 为item设置widget

class Windows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.deal)

    def deal(self):
        all_data = json.loads('[{"ship_name":"uabo",'
                              '"ship_country":"E\u56fd",'
                              '"ship_star":"5",'
                              '"ship_index":"1",'
                              '"ship_photo":"images/bao0.png",'
                              '"ship_type":"\u6218\u5de1"},'
                              '{"ship_name":"\u6d4b\u8bd5",'
                              '"ship_country":"E\u56fd",'
                              '"ship_star":"5",'
                              '"ship_index":"1",'
                              '"ship_photo":"images/bao1.png",'
                              '"ship_type":"\u6218\u5de1"},'
                              '{"ship_name":"\u6d4b\u8bd52",'
                              '"ship_country":"E\u56fd",'
                              '"ship_star":"5",'
                              '"ship_index":"1",'
                              '"ship_photo":"images/bao3.png",'
                              '"ship_type":"\u6218\u5de1"},'
                              '{"ship_name":"\u6d4b\u8bd53",'
                              '"ship_country":"E\u56fd",'
                              '"ship_star":"5",'
                              '"ship_index":"1",'
                              '"ship_photo":"images/bao4.png",'
                              '"ship_type":"\u6218\u5de1"}]')
        def get_item_wight(data):
            # 读取属性
            ship_name = data['ship_name']
            ship_photo = data['ship_photo']
            ship_index = data['ship_index']
            ship_type = data['ship_type']
            ship_country = data['ship_country']
            ship_star = data['ship_star']
            # 总Widget
            wight = QWidget()

            # 总体横向布局
            layout_main = QHBoxLayout()
            map_l = QLabel()  # 头像显示
            map_l.setFixedSize(80, 80)
            maps = QPixmap(ship_photo).scaled(80, 80)
            map_l.setPixmap(maps)

            # 右边的纵向布局
            layout_right = QVBoxLayout()

            # 右下的的横向布局
            layout_right_down = QHBoxLayout()  # 右下的横向布局
            layout_right_down.addWidget(QLabel(ship_type))
            layout_right_down.addWidget(QLabel(ship_country))
            layout_right_down.addWidget(QLabel(str(ship_star) + "星"))
            layout_right_down.addWidget(QLabel(ship_index))

            # 按照从左到右, 从上到下布局添加
            layout_main.addWidget(map_l)  # 最左边的头像

            layout_right.addWidget(QLabel(ship_name))  # 右边的纵向布局
            layout_right.addLayout(layout_right_down)  # 右下角横向布局

            layout_main.addLayout(layout_right)  # 右边的布局

            wight.setLayout(layout_main)  # 布局给wight
            return wight  # 返回wight

        for ship_data in all_data:
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(200, 80))  # 设置QListWidgetItem大小
            widget = get_item_wight(ship_data)  # 调用上面的函数获取对应
            self.listWidget.addItem(item)  # 添加item
            self.listWidget.setItemWidget(item, widget)  # 为item设置widget

listWindows2()
app = QtWidgets.QApplication(sys.argv)
windows = Windows()
windows.show()
sys.exit(app.exec_())
