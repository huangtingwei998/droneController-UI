import sys

import qdarkstyle
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPalette, QIcon
#from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from UImain.opencamera import opencamera
# from CellImageSize import CellImageSize
#from Toolbar import Toolbar, Qt
from UImain.live import LivePage
from UImain.openvideo import VideoPlayer
from UImain.picPlayer import PicPlayer
from UImain.setting import Config, SettingPage
from PyQt5.QtWidgets import QApplication
from Toolbar import DemoWin
from UImain.webcontroller import webWindow
from dataanalysis.datamain import GridLayout

class MyClass(QWidget):
    def __init__(self,name):
        super().__init__()
        self.initUI(name)
        self.resize(1500, 900)
    def f0(self):
        self.stackWidget.setCurrentIndex(0)
    def f1(self):
        self.stackWidget.setCurrentIndex(1)

    def f2(self):
        self.stackWidget.setCurrentIndex(2)

    def f3(self):
        self.stackWidget.setCurrentIndex(3)

    def f4(self):
        self.stackWidget.setCurrentIndex(4)

    def f5(self):
        self.stackWidget.setCurrentIndex(5)

    def f6(self):
        self.stackWidget.setCurrentIndex(6)

    def toolbtnpressed(self, a):
        print("按下的ToolBar按钮是", a.text())  # 打印点击的按钮名称

    def initUI(self,name):
        self.name = name
        self.toolbar = DemoWin(self.name)
        self.config = Config()
        self.setting = SettingPage()
        self.LivePage = LivePage()
        self.Grid = GridLayout()
        self.picPlayer = PicPlayer()
        self.aboutText = QPlainTextEdit()
        self.VideoPlayer = VideoPlayer()

        self.opencamera = opencamera()
        self.web = webWindow()
        self.aboutText.setPlainText(
            """
            本软件是基于计算机视觉的交通检测软件。\n
            目前实现的功能有车辆、行人、人行道、摩托、交通灯等检测。\n
            可实现车辆跟踪和车辆型号检测与车速估计。\n
            可实现对闯红灯、不按导向行驶、超速等违规行为检测和抓拍。\n
            保存必要数据，实现数据可视化。\n
            """
        )
        self.stackWidget = QStackedWidget(self)

        self.setWindowOpacity(1)    #设置窗口透明度
        pe = QPalette()      #调色板
        self.setAutoFillBackground(True)

        self.setPalette(pe)
        self.setWindowTitle("飞行器智能监测系统")

        # self.hwidget = QWidget(self)
        # self.vwidget = QWidget(self)
        self.gwidget = QWidget(self)
        # dk=app.desktop()
        self.vlayout = QVBoxLayout(self)
        self.setGeometry(300, 400, 1200, 818)
        #self.hlayout = QHBoxLayout(self)
        self.grid = QGridLayout()


        #设置6大按钮
        watch_icon = QIcon("./img/watch1.png")
        self.btn_1 = QPushButton(self)
        self.btn_1.setMaximumSize(60, 60)
        self.btn_1.setMinimumSize(60, 60)
        self.btn_1.setIcon(watch_icon)
        self.btn_1.setIconSize(QSize(58, 58))
        self.btn_1.setStyleSheet('''QPushButton{border:none;color:white;font-size:18px;font-family:等线;}
                QPushButton:hover{color:white;
                            border:2px solid #F3F3F5;
                            border-radius:35px;
                            background:darkGray;}''')

        self.btn_2 = QPushButton(self)
        chart_icon = QIcon("./img/chart.png")
        self.btn_2.setMaximumSize(60, 60)
        self.btn_2.setMinimumSize(60, 60)
        self.btn_2.setIcon(chart_icon)
        self.btn_2.setIconSize(QSize(58, 58))
        self.btn_2.setStyleSheet('''QPushButton{border:none;color:white;font-size:18px;font-family:等线;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:35px;
                    background:darkGray;}''')

        self.btn_3 = QPushButton(self)
        pic_icon = QIcon("img/pic.png")
        self.btn_3.setMaximumSize(60, 60)
        self.btn_3.setMinimumSize(60, 60)
        self.btn_3.setIcon(pic_icon)
        self.btn_3.setIconSize(QSize(58, 58))
        self.btn_3.setStyleSheet('''QPushButton{border:none;color:white;font-size:18px;font-family:等线;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:35px;
                    background:darkGray;}''')

        self.btn_4 = QPushButton(self)
        about_icon = QIcon("img/about.png")
        self.btn_4.setMaximumSize(60, 60)
        self.btn_4.setMinimumSize(60, 60)
        self.btn_4.setIcon(about_icon)
        self.btn_4.setIconSize(QSize(58, 58))
        self.btn_4.setStyleSheet('''QPushButton{border:none;color:white;font-size:18px;font-family:等线;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:35px;
                    background:darkGray;}''')

        self.btn_5 = QPushButton(self)
        setting_icon = QIcon("img/setting.png")
        self.btn_5.setMaximumSize(60, 60)
        self.btn_5.setMinimumSize(60, 60)
        self.btn_5.setIcon(setting_icon)
        self.btn_5.setIconSize(QSize(58, 58))
        self.btn_5.setStyleSheet('''QPushButton{border:none;color:white;font-size:18px;font-family:等线;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:35px;
                    background:darkGray;}''')

        self.btn_6 = QPushButton(self)
        live_icon = QIcon("img/live.png")
        self.btn_6.setMaximumSize(60, 60)
        self.btn_6.setMinimumSize(60, 60)
        self.btn_6.setIcon(live_icon)
        self.btn_6.setIconSize(QSize(58, 58))
        self.btn_6.setStyleSheet('''QPushButton{border:none;color:white;font-size:18px;font-family:等线;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:35px;
                    background:darkGray;}''')

        file_icon = QIcon("./img/web.png")
        self.btn_7 = QPushButton(self)
        self.btn_7.setMaximumSize(60, 60)
        self.btn_7.setMaximumSize(60, 60)
        self.btn_7.setIcon(file_icon)
        self.btn_7.setIconSize(QSize(58, 58))
        self.btn_7.setStyleSheet('''QPushButton{border:none;color:white;font-size:18px;font-family:等线;}
                QPushButton:hover{color:white;
                            border:2px solid #F3F3F5;
                            border-radius:35px;
                            background:darkGray;}''')

        self.btn_1.clicked.connect(self.f0)
        self.btn_2.clicked.connect(self.f1)
        self.btn_3.clicked.connect(self.f2)
        self.btn_4.clicked.connect(self.f3)
        self.btn_5.clicked.connect(self.f4)
        self.btn_6.clicked.connect(self.f5)
        self.btn_7.clicked.connect(self.f6)

        self.grid.addWidget(self.btn_1, 0, 0)
        self.grid.addWidget(self.btn_2, 1, 0)
        self.grid.addWidget(self.btn_3, 2, 0)
        self.grid.addWidget(self.btn_4, 3, 0)
        self.grid.addWidget(self.btn_5, 4, 0)
        self.grid.addWidget(self.btn_6, 5, 0)
        self.grid.addWidget(self.btn_7, 6, 0)

        self.grid.addWidget(self.stackWidget, 0, 1, 7, 5)
        self.stackWidget.addWidget(self.LivePage)
        self.stackWidget.addWidget(self.Grid)
        self.stackWidget.addWidget(self.picPlayer)
        self.stackWidget.addWidget(self.aboutText)
        self.stackWidget.addWidget(self.setting)
        self.stackWidget.addWidget(self.VideoPlayer)
        # self.stackWidget.addWidget(self.opencamera)
        self.stackWidget.addWidget(self.web)
        self.gwidget.setLayout(self.grid)
        self.vlayout.addWidget(self.toolbar)
        self.vlayout.addWidget(self.gwidget, 16)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mc = MyClass("huang")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.exec()
