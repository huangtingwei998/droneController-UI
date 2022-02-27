import json
import os
import shutil
import sys

import qdarkstyle
from PyQt5 import QtWidgets

# from vtk1.pyqtvtk import VTKWindow
from login.SignIn import SignInWidget
from myserial.pyserial_main import Pyqt5_Serial
# 导入QT,其中包含一些常量，例如颜色等
from PyQt5.QtCore import Qt, QSize
# 导入常用组件
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QWidget, QLabel, QVBoxLayout, \
    QLineEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QAction
# 使用调色板等
from PyQt5.QtGui import QIcon, QPixmap
from mapUI.mapBrower import MapWindow

class DemoWin(QMainWindow):
    def __init__(self,name):
        super().__init__()
        self.initUI(name)
    def initUI(self,name):
        self.aboutText = QPlainTextEdit()
        self.aboutText.setPlainText(
            """
            本软件是基于计算机视觉的交通检测软件。\n
            目前实现的功能有车辆、行人、人行道、摩托、交通灯等检测。\n
            可实现车辆跟踪和车辆型号检测与车速估计。\n
            可实现对闯红灯、不按导向行驶、超速等违规行为检测和抓拍。\n
            保存必要数据，实现数据可视化。\n
            """
        )
        self.resize(400, 250)
        # 创建一个toolBar，用于放置文件操作
        fileBar = self.addToolBar("File")
        new = QAction(QIcon('./img/new.PNG'), "新建", self)  # 指定了图标默认显示图标

        new.triggered.connect(lambda: self.newproject())
        fileBar.addAction(new)

        open = QAction(QIcon('./img/file.png'), "打开", self)
        fileBar.addAction(open)
        open.triggered.connect(lambda: self.updataproject())

        save = QAction(QIcon('./img/save.png'), "保存", self)
        fileBar.addAction(save)
        save.triggered.connect(lambda: self.saveproject())
        fileBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置名称显示在图标下面（默认本来是只显示图标）

        # 创建另一个toolbar，用于放置编辑操作
        appBar = self.addToolBar("app")
        zitai = QAction(QIcon('./img/3d.PNG'), "姿态显示", self)  # 指定了图标默认显示图标
        zitai.triggered.connect(lambda: self.VTK())
        appBar.addAction(zitai)
        map = QAction(QIcon('./img/map.png'), "地图定位", self)
        map.triggered.connect(lambda: self.map())
        appBar.addAction(map)
        height = QAction(QIcon('./img/height.PNG'), "高度显示", self)
        appBar.addAction(height)
        see = QAction(QIcon('./img/see.PNG'), "查看远程", self)
        appBar.addAction(see)
        serial = QAction(QIcon('./img/serial.PNG'), "串口助手", self)
        serial.triggered.connect(lambda: self.serial())
        appBar.addAction(serial)
        appBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置名称显示在图标下面（默认本来是只显示图标）

        # 创建另一个toolbar，用于放置编辑操作
        helpBar = self.addToolBar("about")
        help = QAction(QIcon('./img/help.PNG'), "帮助", self)  # 指定了图标默认显示图标
        helpBar.addAction(help)
        about = QAction(QIcon('./img/about.png'), "关于我们", self)
        helpBar.addAction(about)
        about.triggered.connect(lambda: self.aboutText)
        soc = QAction(QIcon('./img/soc.PNG'), "社区支持", self)
        helpBar.addAction(soc)
        helpBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置名称显示在图标下面（默认本来是只显示图标）
        helpBar.setFixedWidth(800)

        login = self.addToolBar("login")
        login1 = QAction(QIcon('./img/login.PNG'), name, self)  # 指定了图标默认显示图标
        login.addAction(login1)

        login1.triggered.connect(lambda:self.login())
        login.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def login(self):
        self.loginwindow = SignInWidget()
    def map(self):
        self.map = MapWindow()
    # def VTK(self):
        # self.VTK = VTKWindow()
    def serial(self):
        self.serial = Pyqt5_Serial()

    # 新建项目
    def newproject(self):
        self.newproject = projectWindows()
    # 修改项目地址
    def updataproject(self):
        self.updataproject = updataprojectWindows()
    # 项目另存为
    def saveproject(self):
        self.saveproject = saveprojectWindows()

    def systemdirectory(self):
        directory1 = QFileDialog.getExistingDirectory(self,"选取文件夹","./")  # 起始路径
        sys = {
            'system': directory1
        }
        with open('config/system.json', 'w') as f:
            json.dump(sys, f)
        print(directory1)

#         项目另存为
class saveprojectWindows(QWidget):
    def __init__(self):
        super(saveprojectWindows, self).__init__()

        self.projectname = QLabel("原项目地址：")  # 头像显示
        self.projectlocal = QLabel("另存为地址：")

        self.projectnamelineedit = QLineEdit()
        self.projectlocallineedit = QLineEdit()
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.projectname)
        hlayout1.addWidget(self.projectnamelineedit)


        self.btn = QPushButton(self)
        chart_icon = QIcon("./img/file.png")
        self.btn.setMaximumSize(25, 25)
        self.btn.setMinimumSize(25, 25)
        self.btn.setIcon(chart_icon)
        self.btn.setIconSize(QSize(24, 24))
        self.btn.clicked.connect(self.systemdirectory)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.projectlocal)
        hlayout2.addWidget(self.projectlocallineedit)
        hlayout2.addWidget(self.btn)
        self.button_save = QtWidgets.QPushButton("确定")
        self.button_save.setFixedWidth(80)
        self.button_save.setFixedHeight(30)
        self.button_save.setStyleSheet("QPushButton{color:black}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{background-color:rgb(78,255,255)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")
        self.button_save.clicked.connect(self.finaldirectory)
        self.warningtext = QLabel()
        hlayout = QVBoxLayout()
        hlayout.addLayout(hlayout1)
        hlayout.addLayout(hlayout2)
        hlayout.addWidget(self.button_save)
        hlayout.addWidget(self.warningtext)

        self.setLayout(hlayout)
        self.setWindowTitle("另存项目为")
        self.resize(400,200)
        with open("config/system.json", "r") as f:
            dict = json.load(f)
        self.localstr = dict['system']
        self.projectnamelineedit.setText(self.localstr)
        self.show()
    def systemdirectory(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        self.projectlocallineedit.setText(directory1)

    def finaldirectory(self):
        path= self.projectlocallineedit.text()
        # 判断文件夹是否存在
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            sys = {
                'system': path
            }
            with open('config/system.json', 'w') as f:
                json.dump(sys, f)
                print(self.localstr)
                print(path)
            shutil.copytree(self.localstr, path)
            QMessageBox.warning(self, "另存为成功", "项目路径为" + path, QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "警告", "此文件夹" + path+"已经存在，继续操作？", QMessageBox.Yes, QMessageBox.Yes)



class updataprojectWindows(QWidget):
    def __init__(self):
        super(updataprojectWindows, self).__init__()

        self.projectname = QLabel("原项目地址：")  # 头像显示
        self.projectlocal = QLabel("修改项目地址：")

        self.projectnamelineedit = QLineEdit()
        self.projectlocallineedit = QLineEdit()
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.projectname)
        hlayout1.addWidget(self.projectnamelineedit)


        self.btn = QPushButton(self)
        chart_icon = QIcon("./img/file.png")
        self.btn.setMaximumSize(25, 25)
        self.btn.setMinimumSize(25, 25)
        self.btn.setIcon(chart_icon)
        self.btn.setIconSize(QSize(24, 24))
        self.btn.clicked.connect(self.systemdirectory)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.projectlocal)
        hlayout2.addWidget(self.projectlocallineedit)
        hlayout2.addWidget(self.btn)
        self.button_save = QtWidgets.QPushButton("确定")
        self.button_save.setFixedWidth(80)
        self.button_save.setFixedHeight(30)
        self.button_save.setStyleSheet("QPushButton{color:black}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{background-color:rgb(78,255,255)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")
        self.button_save.clicked.connect(self.finaldirectory)
        self.warningtext = QLabel()
        hlayout = QVBoxLayout()
        hlayout.addLayout(hlayout1)
        hlayout.addLayout(hlayout2)
        hlayout.addWidget(self.button_save)
        hlayout.addWidget(self.warningtext)

        self.setLayout(hlayout)
        self.setWindowTitle("打开项目")
        self.resize(400,200)
        with open("config/system.json", "r") as f:
            dict = json.load(f)
        self.localstr = dict['system']
        self.projectnamelineedit.setText(self.localstr)
        self.show()
    def systemdirectory(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        self.localstr = directory1
        self.projectlocallineedit.setText(self.localstr)

    def finaldirectory(self):
        path= self.projectlocallineedit.text()
        # 判断文件夹是否存在
        isExists = os.path.exists(path)
        if not isExists:
            QMessageBox.warning(self, "警告", "此文件夹不存在" + path, QMessageBox.Yes, QMessageBox.Yes)
        else:
            sys = {
                'system': path+"/"
            }
            with open('config/system.json', 'w') as f:
                json.dump(sys, f)
            QMessageBox.warning(self, "修改成功", "项目路径为" + path, QMessageBox.Yes, QMessageBox.Yes)


class projectWindows(QWidget):
    def __init__(self):
        super(projectWindows, self).__init__()

        self.projectname = QLabel("项目名称：")  # 头像显示
        self.projectlocal = QLabel("项目位置：")

        self.projectnamelineedit = QLineEdit()
        self.projectnamelineedit.textChanged.connect(self.lineedit)
        self.projectlocallineedit = QLineEdit()
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.projectname)
        hlayout1.addWidget(self.projectnamelineedit)


        self.btn = QPushButton(self)
        chart_icon = QIcon("./img/file.png")
        self.btn.setMaximumSize(25, 25)
        self.btn.setMinimumSize(25, 25)
        self.btn.setIcon(chart_icon)
        self.btn.setIconSize(QSize(24, 24))
        self.btn.clicked.connect(self.systemdirectory)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.projectlocal)
        hlayout2.addWidget(self.projectlocallineedit)
        hlayout2.addWidget(self.btn)
        self.button_save = QtWidgets.QPushButton("确定")
        self.button_save.setFixedWidth(80)
        self.button_save.setFixedHeight(30)
        self.button_save.setStyleSheet("QPushButton{color:black}"
                                      "QPushButton:hover{color:red}"
                                      "QPushButton{background-color:rgb(78,255,255)}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")
        self.button_save.clicked.connect(self.finaldirectory)
        self.warningtext = QLabel()
        hlayout = QVBoxLayout()
        hlayout.addLayout(hlayout1)
        hlayout.addLayout(hlayout2)
        hlayout.addWidget(self.button_save)
        hlayout.addWidget(self.warningtext)

        self.setLayout(hlayout)
        self.setWindowTitle("新建项目")
        self.resize(400,200)
        self.localstr = "C:/Users/huangtingwei/Desktop/"
        self.projectlocallineedit.setText(self.localstr)
        self.show()
    def lineedit(self):
        project = self.projectnamelineedit.text()
        self.projectlocallineedit.setText(self.localstr+project)
    def systemdirectory(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        self.projectlocallineedit.setText(directory1)
        self.localstr = directory1 + "/"
        project = self.projectnamelineedit.text()
        self.projectlocallineedit.setText(self.localstr + project)

    def finaldirectory(self):
        path= self.projectlocallineedit.text()+"/"
        # 判断文件夹是否存在
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            sys = {
                'system': path
            }
            with open('config/system.json', 'w') as f:
                json.dump(sys, f)
            QMessageBox.warning(self, "新建成功", "项目路径为"+path, QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "警告", "该文件夹已经存在", QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("img/pic.png"))
    # 创建一个主窗口
    mainWin = DemoWin("huang")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())
