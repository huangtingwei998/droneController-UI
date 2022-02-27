import qdarkstyle
from PyQt5.QtCore import Qt
import os
from PIL import Image
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UImain.opencamera import opencamera

class listWindows(QMainWindow):
    def __init__(self,listWidget):
        super(listWindows, self).__init__()
        self.listWidget = listWidget
        timer = QTimer(self)
        timer.timeout.connect(self.deal)
        timer.start(1000)
        self.list = []

    def readimage(self,each_file):
        data = []
        # all_files = os.listdir("face")  # os.curdir 表示当前目录 curdir:currentdirectory
        # type_dict = dict()
        # for each_file in all_files:
        # 如果不是文件夹，而是文件，统计我们的文件
        file_name, ext = os.path.splitext(each_file)  # 获取到文件的后缀
        fsize = os.path.getsize("face/" + each_file)

        im = Image.open("face/" + each_file)  # 返回一个Image对象
        width = im.size[0]
        higth = im.size[1]

        data.append(str(file_name))
        data.append(str(ext))
        data.append(str(fsize))
        data.append(str(width))
        data.append(str(higth))
        return data
    def get_item_wight(self,data,each_file):
            # 读取属性
            ship_name = data[0]
            ship_photo = each_file
            ship_index = data[1]
            ship_type = data[2]
            ship_country = data[3]
            ship_star = data[4]
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
            layout_right_down.addWidget(QLabel(str(ship_type)+"B"))
            layout_right_down.addWidget(QLabel(str(ship_country)))
            layout_right_down.addWidget(QLabel(str(ship_star)))
            layout_right_down.addWidget(QLabel(str(ship_index)))

            # 按照从左到右, 从上到下布局添加
            layout_main.addWidget(map_l)  # 最左边的头像

            layout_right.addWidget(QLabel(str(ship_name)))  # 右边的纵向布局
            layout_right.addLayout(layout_right_down)  # 右下角横向布局

            layout_main.addLayout(layout_right)  # 右边的布局

            groupBox2 = QGroupBox()
            groupBox2.setLayout(layout_main)
            groupBox2.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            # 将groupbox封装进layoutfinal
            layoutfinal = QVBoxLayout()
            layoutfinal.addWidget(groupBox2)
            wight.setLayout(layoutfinal)  # 布局给wight
            return wight  # 返回wight

    def deal(self):
        all_files = os.listdir("face")  # os.curdir 表示当前目录 curdir:currentdirectory
        for each_file in all_files:
            ship_data = self.readimage(each_file)
            if ship_data in self.list:
                pass
            else:
                self.list.append(ship_data)
                item = QListWidgetItem()  # 创建QListWidgetItem对象
                item.setSizeHint(QSize(200, 130))  # 设置QListWidgetItem大小
                widget = self.get_item_wight(ship_data,"face/"+each_file)  # 调用上面的函数获取对应
                self.listWidget.addItem(item)  # 添加item
                self.listWidget.setItemWidget(item, widget)  # 为item设置widget


class itemswindow(QWidget):
    def __init__(self,data,file,each_file):
        super(itemswindow, self).__init__()
        self.ship_name = data
        # 总体横向布局
        layout_main = QHBoxLayout()
        # 数据库图片
        map_l = QLabel()  # 头像显示
        # map_l.setFixedSize(80, 80)
        maps = QPixmap(file).scaled(80, 80)
        map_l.setPixmap(maps)
        # 采集的图片
        map_l1 = QLabel()  # 头像显示
        # map_l1.setFixedSize(80, 80)
        maps1 = QPixmap(each_file).scaled(80, 80)
        map_l1.setPixmap(maps1)
        # 最又的布局
        hlayout = QVBoxLayout()
        if self.ship_name!="unkown":
            text = QLabel(str("识别到" + self.ship_name))
            buttun = QPushButton("详情")
            buttun.clicked.connect(self.ClickBtn)  # 连接点击槽
            hlayout.addWidget(text)
            hlayout.addWidget(buttun)
            layout_main.addWidget(map_l)  # 最左边的头像
            layout_main.addWidget(map_l1)
            layout_main.addLayout(hlayout)
        else:
            text = QLabel("未识别到")
            layout_main.addWidget(map_l)  # 最左边的头像
            layout_main.addWidget(map_l1)
            layout_main.addWidget(text)


        self.groupBox2 = QGroupBox(self.ship_name)
        self.groupBox2.setLayout(layout_main)
        self.groupBox2.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        layoutfinal = QHBoxLayout()
        layoutfinal.addWidget(self.groupBox2)
        self.setLayout(layoutfinal)  # 布局

    def ClickBtn(self):
        self.win  = nameWindows(self.ship_name)




class nameWindows(QWidget):
    def __init__(self,name):
        super(nameWindows, self).__init__()
        maps = QPixmap("face_dataset/"+ name +".JPG").scaled(160, 160)
        self.name = name
        self.nametxt=""
        with open('config/name.txt', 'r', encoding='UTF-8') as f:
            for line in f:
                txtname = line.strip('\n')
                if self.name==txtname.split(':')[0]:
                    self.nametxt=txtname.split(':')[1]

        self.map_l1 = QLabel()  # 头像显示
        self.map_l1.setPixmap(maps)
        self.text = QLabel(str("人物：" + self.name))
        self.mametextlabel = QLabel(self.nametxt)
        hlayout = QVBoxLayout()
        hlayout.addWidget(self.map_l1)
        hlayout.addWidget(self.text)
        hlayout.addWidget(self.mametextlabel)
        self.setLayout(hlayout)
        self.mametextlabel.setFixedWidth(200)
        self.setWindowTitle(self.name)
        self.show()

class listWindows2(QMainWindow):
    def __init__(self,listWidget):
        super(listWindows2, self).__init__()
        self.listWidget = listWidget
        self.list = []
        timer = QTimer(self)
        timer.timeout.connect(self.deal)
        timer.start(1000)


    def searchimage(self,each_file):
        name = each_file.split("_")[0]+"."+each_file.split(".")[1]
        file_name, ext = os.path.splitext(name)  # 获取到文件的后缀
        all_files = os.listdir("face_dataset")  # os.curdir 表示当前目录 curdir:currentdirectory
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
            wight = itemswindow(data,file,each_file)
            return wight  # 返回wight

    def deal(self):
        all_files = os.listdir("face")  # os.curdir 表示当前目录 curdir:currentdirectory
        for each_file in all_files:
            image,filename = self.searchimage(each_file)
            if filename in self.list:
                pass
            else:
                self.list.append(filename)
                item = QListWidgetItem()  # 创建QListWidgetItem对象
                item.setSizeHint(QSize(200, 120))  # 设置QListWidgetItem大小
                widget = self.get_item_wight(filename,image,"face/"+each_file)  # 调用上面的函数获取对应data,file,each_file
                self.listWidget.addItem(item)  # 添加item
                self.listWidget.setItemWidget(item, widget)  # 为item设置widget



class LivePage(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        # 建立三个DockWidget
        self.screenDockWidget = QDockWidget(self)
        self.carInforDockWidget = QDockWidget(self)
        self.faceDockWidget = QDockWidget(self)

        # 建立三个界面
        self.listWidget = QListWidget(self)
        self.listWidget.setFixedWidth(250)
        self.listWidget2 = QListWidget(self)
        self.listWidget2.setFixedWidth(250)
        self.detectscreen = opencamera()
        # 将livepage的三个窗口传入各自的listwindow
        self.listWindows = listWindows(self.listWidget)
        self.listWindows2 = listWindows2(self.listWidget2)

        # 将三个界面布局
        self.addDockWidget(Qt.RightDockWidgetArea, self.faceDockWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.screenDockWidget)
        self.splitDockWidget(self.faceDockWidget, self.carInforDockWidget, Qt.Vertical)
        self.screenDockWidget.setWidget(self.detectscreen)
        self.carInforDockWidget.setWidget(self.listWidget)
        self.carInforDockWidget.setWindowTitle("目标跟踪窗口")
        self.detectscreen.setStyleSheet("background-color: white")
        self.faceDockWidget.setWidget(self.listWidget2)
        self.faceDockWidget.setWindowTitle("人脸识别窗口")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    player=LivePage()
    player.show()
    sys.exit(app.exec_())
