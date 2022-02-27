import sys

import numpy as np
import psutil
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QGridLayout, QFrame, QLabel, QPushButton, QHBoxLayout, QWidget
import pyqtgraph as pg


class curveExample(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.generate_image()

        timer = QTimer(self)
        timer.timeout.connect(self.plotData)
        timer.start(100)
    def InitUi(self):
        self.setGeometry(200,200,400,200)
        self.setWindowTitle("实时刷新波形实验")
        self.gridLayout = QGridLayout(self)
        self.frame = QFrame(self)      #创建一个父容器
        self.frame.setFrameShape(QFrame.Panel)   #设置父容器的面板形式
        self.frame.setFrameShadow(QFrame.Plain)  #设置父容器边框阴影。
        self.frame.setLineWidth(2)               #设置父容器边框线宽
        self.frame.setStyleSheet("background-color:rgb(0,255,255);")  #设置表单颜色
        self.gridLayout.addWidget(self.frame,0,0,1,2)   #griflayout的使用，将frame容器放在grid得一行
        self.setLayout(self.gridLayout)

    def generate_image(self):
        verticalLayout = QHBoxLayout(self.frame)   #创建父容器后需要将graph添加到里面，采用QVBoxLaouth或者QHBoxLayout
        win = pg.GraphicsLayoutWidget(self.frame)  #将其显示在frame上
        verticalLayout.addWidget(win)
        p = win.addPlot(title = "动态波形图")
        p.showGrid(x=True,y=True)
        p.setLabel(axis="left",text ="Y Value")
        p.setLabel(axis="bottom",text="X Value")
        p.setTitle("数据分析")
        p.addLegend()

        self.curve1 = p.plot(pen="r",name="y1")
        self.curve2 = p.plot(pen='g',name="y2")

        self.Fs = 20 #采样频率
        self.N = 400    #采样点数
        self.f0 = 4.0    #信号频率
        self.pha = 0     #初试相位

        self.t = np.arange(self.N) /self.Fs    #时间向量1*1024的矩阵

        l = 20
        lis = [0] * l
        self.y = lis

    def plotData(self):
        cpu = "%0.2f" % psutil.cpu_percent(interval=1)
        self.y[:-1] = self.y[1:]
        self.y[-1] = float(cpu)
        self.curve1.setData(self.y)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = curveExample()
    ex.show()
    sys.exit(app.exec_())
