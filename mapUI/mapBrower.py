# v1.2
# created
#   by Roger
# in 2017.1.3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from mapUI.map import mapmain
import sys

class MapWindow(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('飞行器智能监测系统地图定位插件')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icons/penguin.png'))
        # 设置窗口大小900*600
        self.resize(900, 600)
        self.show()

        # 设置浏览器控件
        self.browser = QWebEngineView()

        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')

        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))

        # navigation_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置名称显示在图标下面（默认本来是只显示图标）
        #QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('img/icons/back.png'), '返回', self)
        next_button = QAction(QIcon('img/icons/next.png'), '前进', self)
        stop_button = QAction(QIcon('img/icons/stop.png'), '停止', self)
        reload_button = QAction(QIcon('img/icons/reload.png'), '重载', self)

        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        self.URLtext = QLabel('URL地址')
        #添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.URLtext)
        navigation_bar.addWidget(self.urlbar)
        #让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)


        # 设置智能输入浮点数
        double = QDoubleValidator(self)
        # 设置经度和纬度的文本控件
        self.longitude = QLineEdit()
        self.longitude.returnPressed.connect(self.changemap)
        self.longitude.setValidator(double)
        self.longitudetext = QLabel('经度')
        self.latitude = QLineEdit()
        self.latitude.returnPressed.connect(self.changemap)
        self.latitude.setValidator(double)
        self.latitudetext = QLabel('纬度')
        navigation_bar.addWidget(self.longitudetext)
        navigation_bar.addWidget(self.longitude)
        navigation_bar.addWidget(self.latitudetext)
        navigation_bar.addWidget(self.latitude)
        # 设置地图类型，默认有高德和谷歌
        self.maptype = QLabel('地图类型')
        navigation_bar.addWidget(self.maptype)
        self.cbx = QComboBox(self)
        self.cbx.addItem("请选择地图类型")
        self.cbx.addItem("高德街道图")
        self.cbx.addItem("高德卫星图")
        self.cbx.addItem("谷歌卫星图")
        self.cbx.addItem("谷歌街道图")
        self.cbx.setCurrentIndex(1)  # 设置默认值
        self.cbx.currentIndexChanged.connect(self.changemap)
        navigation_bar.addWidget(self.cbx)

        # 初始化URL地址
        [longitudedata,latitudedata] = self.getGPS()
        url = 'C:/Users/huang/Desktop/文件夹/飞行器pythonProject17/mapUI/' + mapmain(1, [39.9075,116.3975])
        # url = 'https://www.baidu.com/'
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
    #     默认地址为北京天安门
    def getGPS(self):
        longitudedata = self.longitude.text()
        latitudedata = self.latitude.text()
        if longitudedata  == "":
            longitudedata = 39.9075
        if latitudedata == "":
            latitudedata  = 116.3975
        longitudedata = float(longitudedata)
        latitudedata = float(latitudedata)
        print(longitudedata,latitudedata)
        return longitudedata,latitudedata
    def getmaptype(self):
        type=1
        typetext = self.cbx.currentText()
        if typetext=="高德卫星图":
            type = 2
        elif typetext=="谷歌卫星图":
            type = 3
        elif typetext=="谷歌街道图":
            type = 4
        else:
            type = 1
        print(type)
        return type
    def changemap(self):
        [longitudedata, latitudedata] = self.getGPS()
        type = self.getmaptype()
        url = 'C:/Users/huang/Desktop/文件夹/飞行器pythonProject17/mapUI/' + mapmain(type, [longitudedata, latitudedata])
        self.browser.setUrl(QUrl(url))


if __name__ == '__main__':
    # 创建应用
    app = QApplication(sys.argv)
    # 创建主窗口
    window = MapWindow()
    # 显示窗口
    window.show()
    # 运行应用，并监听事件
    app.exec_()
