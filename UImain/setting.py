import json
import os
import sys

import qdarkstyle
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTextEdit
class Config:
    def __init__(self):
        # 权重管理
        self.YOLOWEIGHT="./weights/yolov5x.pt"
        self.DEEPSORTWEIGHRT ="./deep_sort/deep/checkpoint/ckpt.t7"
        self.modellocal = "./vtk1/resource/Drone-Tla.STL"
        self.facenetWEIGHT = ""
        # 类别检测
        self.personisdetect = True
        self.bicycleisdetect=True
        self.carisdetect = True
        self.motorcycleisdetect = True
        self.busisdetect = True
        self.truckisdetect = True
        # 网址管理
        self.remoteURL = ""
        self.societysupport = ""
        # 系统路径
        self.systemURL = ""
        # 数据保存
        self.detectresult= True
        self.facenetresult = True
        self.IDtrackerresult = True
        # 传感器数据
        self.mpu6050data = True
        self.GPSdata = True
        self.heightdata = True


class SettingPage(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QGridLayout()
        layout1=QGridLayout()
        yolov5_label=QLabel('yolov5权重')
        layout1.addWidget(yolov5_label,0,0)#将label组件加入到布局layout中，后面参数标示行下标，列下标
        yolov5_titleEdit=QLineEdit()   #单行输入文本
        layout1.addWidget(yolov5_titleEdit,0,1)
        yolov5btn = QPushButton("选择权重")
        layout1.addWidget(yolov5btn, 0, 2)

        deepsort_label = QLabel('deepsort权重')
        layout1.addWidget(deepsort_label, 1, 0)
        deepsortEdit = QLineEdit() #单行输入文本
        layout1.addWidget(deepsortEdit, 1, 1)
        deepsortbtn = QPushButton("选择权重")
        layout1.addWidget(deepsortbtn, 1, 2)

        face_label=QLabel('人脸识别权重')
        layout1.addWidget(face_label,2,0)
        face_descEdit=QLineEdit()    #多行输入文本
        layout1.addWidget(face_descEdit,2,1)
        facebtn = QPushButton("选择权重")
        layout1.addWidget(facebtn, 2, 2)

        model_label=QLabel('姿态模型位置')
        layout1.addWidget(model_label,3,0)
        model_descEdit=QLineEdit()    #多行输入文本
        layout1.addWidget(model_descEdit,3,1)
        modelbtn = QPushButton("选择模型")
        layout1.addWidget(modelbtn, 3, 2)
        self.groupBox1 = QGroupBox("资源设置")
        self.groupBox1.setLayout(layout1)
        main_layout.addWidget(self.groupBox1,0,0)

        layout2 = QGridLayout()
        remote_label = QLabel('远程管理网址')
        layout2.addWidget(remote_label, 0, 0)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        remoteEdit = QLineEdit()  # 单行输入文本
        layout2.addWidget(remoteEdit, 0, 1)

        support_label = QLabel('社交支持网址')
        layout2.addWidget(support_label, 1, 0)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        supportEdit = QLineEdit()  # 单行输入文本
        layout2.addWidget(supportEdit, 1, 1)

        remote_label = QLabel('工程地址设置')
        layout2.addWidget(remote_label, 2, 0)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        remoteEdit = QLineEdit()  # 单行输入文本
        layout2.addWidget(remoteEdit, 2, 1)
        self.groupBox2 = QGroupBox("地址设置")
        self.groupBox2.setLayout(layout2)
        main_layout.addWidget(self.groupBox2,0,1)

        layout3 = QGridLayout()
        person_label = QLabel('行人检测')
        layout3.addWidget(person_label, 0, 0)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        personchoice = QComboBox()
        personchoice.addItem("是")
        personchoice.addItem("否")
        layout3.addWidget(personchoice, 0, 1)

        bicycle_label = QLabel('自行车检测')
        layout3.addWidget(bicycle_label, 0, 2)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        bicyclechoice = QComboBox()
        bicyclechoice.addItem("是")
        bicyclechoice.addItem("否")
        layout3.addWidget(bicyclechoice, 0, 3)

        car_label = QLabel('轿车检测')
        layout3.addWidget(car_label, 0, 4)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        carchoice = QComboBox()
        carchoice.addItem("是")
        carchoice.addItem("否")
        layout3.addWidget(carchoice, 0, 5)

        motorcycle_label = QLabel('摩托检测')
        layout3.addWidget(motorcycle_label, 1, 0)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        motorcyclechoice = QComboBox()
        motorcyclechoice.addItem("是")
        motorcyclechoice.addItem("否")
        layout3.addWidget( motorcyclechoice, 1, 1)

        bus_label = QLabel('公交检测')
        layout3.addWidget(bus_label, 1, 2)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        buschoice = QComboBox()
        buschoice.addItem("是")
        buschoice.addItem("否")
        layout3.addWidget(buschoice, 1, 3)

        truck_label = QLabel('其他交通')
        layout3.addWidget(truck_label, 1, 4)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        truckchoice = QComboBox()
        truckchoice.addItem("是")
        truckchoice.addItem("否")
        layout3.addWidget(truckchoice, 1, 5)

        self.groupBox3 = QGroupBox("类别检测设置")
        self.groupBox3.setLayout(layout3)
        main_layout.addWidget(self.groupBox3,1,0)

        layout4 = QGridLayout()
        detect_label = QLabel('目标检测结果')
        layout4.addWidget(detect_label, 0, 0)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        detectchoice = QComboBox()
        detectchoice.addItem("是")
        detectchoice.addItem("否")
        layout4.addWidget(detectchoice, 0, 1)

        face_label = QLabel('人脸识别结果')
        layout4.addWidget(face_label, 0, 2)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        facechoice = QComboBox()
        facechoice.addItem("是")
        facechoice.addItem("否")
        layout4.addWidget(facechoice, 0, 3)

        IDtracker_label = QLabel('ID追踪结果')
        layout4.addWidget(IDtracker_label, 0, 4)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        IDtrackerchoice = QComboBox()
        IDtrackerchoice.addItem("是")
        IDtrackerchoice.addItem("否")
        layout4.addWidget(IDtrackerchoice, 0, 5)

        mpudata_label = QLabel('姿态传感数据')
        layout4.addWidget(mpudata_label, 1, 0)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        mpudatachoice = QComboBox()
        mpudatachoice.addItem("是")
        mpudatachoice.addItem("否")
        layout4.addWidget(mpudatachoice, 1, 1)

        GPSdata_label = QLabel('GPS数据')
        layout4.addWidget(GPSdata_label, 1, 2)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        GPSdatachoice = QComboBox()
        GPSdatachoice.addItem("是")
        GPSdatachoice.addItem("否")
        layout4.addWidget(GPSdatachoice, 1, 3)

        heightdata_label = QLabel('高度数据')
        layout4.addWidget(heightdata_label, 1, 4)  # 将label组件加入到布局layout中，后面参数标示行下标，列下标
        heightdatachoice = QComboBox()
        heightdatachoice.addItem("是")
        heightdatachoice.addItem("否")
        layout4.addWidget(heightdatachoice, 1, 5)

        self.groupBox4 = QGroupBox("数据保存设置")
        self.groupBox4.setLayout(layout4)
        main_layout.addWidget(self.groupBox4,1,1)

        layout5 = QGridLayout()
        self.groupBox5 = QGroupBox("人脸数据库管理")
        self.groupBox5.setLayout(layout5)
        persondatachoice = QComboBox()
        persondatachoice.addItem("增加")
        persondatachoice.addItem("修改")
        persondatachoice.addItem("删除")
        personname = QLabel("姓名")
        personimage = QLabel("图片")
        personmes = QLabel("描述")
        personnameedit = QLineEdit()
        personimageedit = QLineEdit()
        presonbtn = QPushButton("选择")
        personmesedit = QTextEdit()
        personfinsh = QPushButton("完成")
        layout5.addWidget(persondatachoice,0,0)
        layout5.addWidget(personname, 0, 1)
        layout5.addWidget(personnameedit, 0, 2,1,2)
        layout5.addWidget(personimage, 1, 1)
        layout5.addWidget(personimageedit, 1, 2)
        layout5.addWidget(presonbtn, 1, 3)
        layout5.addWidget(personmes, 2, 1)
        layout5.addWidget(personmesedit, 2, 2,2,2)
        layout5.addWidget(personfinsh, 4, 0,1,2)

        main_layout.addWidget(self.groupBox5, 2, 0)

        layout6 = QGridLayout()
        self.groupBox6 = QGroupBox("用户个人资料管理")
        username = QLabel("姓名")
        userimage = QLabel("头像")
        usertelephone = QLabel("电话")
        usermail = QLabel("邮箱")
        usernameedit = QLineEdit()
        userimageedit = QLineEdit()
        usertelephoneedit = QLineEdit()
        userbtn = QPushButton("选择")
        usermailedit = QLineEdit()
        userbtn1 =  QPushButton("完成")
        layout6.addWidget(username,0,0)
        layout6.addWidget(usernameedit,0,1,1,2)
        layout6.addWidget(userimage,1,0)
        layout6.addWidget(userimageedit,1,1)
        layout6.addWidget(userbtn,1,2)
        layout6.addWidget(usertelephone,2,0)
        layout6.addWidget(usertelephoneedit,2,1,1,2)
        layout6.addWidget(usermail,3,0)
        layout6.addWidget(usermailedit,3,1,1,2)
        layout6.addWidget(userbtn1, 4, 0)
        self.groupBox6.setLayout(layout6)
        main_layout.addWidget(self.groupBox6, 2, 1)

        self.setLayout(main_layout)
        self.show()

if __name__=='__main__':
    app=QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    e=SettingPage()

    sys.exit(app.exec())