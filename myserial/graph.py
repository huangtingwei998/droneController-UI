from PyQt5.QtWidgets import QPushButton,QWidget,QApplication,QGridLayout,QListWidget,QLineEdit
import pyqtgraph as pg
import sys
import numpy as np


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.linePlot()
        self.scatterPlot()
        self.three_curves()

    def initUI(self):
        self.setGeometry(400,400,800,620)
        self.setWindowTitle("pyqtgraph快速入门")

        ## 创建一些小部件放在顶级窗口中
        btn = QPushButton('press me')
        text = QLineEdit('enter text')
        listw = QListWidget()
        listw.addItems(["aa", "bb", "cc"])

        self.gridLayout = QGridLayout(self)
        ## 将部件添加到布局中的适当位置
        self.gridLayout.addWidget(btn, 0, 0)
        self.gridLayout.addWidget(text, 1, 0)
        self.gridLayout.addWidget(listw, 2, 0)

        self.setLayout(self.gridLayout)

    def linePlot(self):
        plt1 = pg.PlotWidget()
        plt1.plot([i for i in range(10)], [i * i for i in range(10)])
        self.gridLayout.addWidget(plt1, 0, 1, 1, 1)

    def scatterPlot(self):
        plt2 = pg.PlotWidget()
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        plt2.plot(x, y, pen=None, symbol="o")
        self.gridLayout.addWidget(plt2, 1, 1, 1, 1)

    def three_curves(self):
        plt3 = pg.PlotWidget(title="Three plot curves")
        x = np.arange(1000)
        y = np.random.normal(size=(3, 1000))
        for i in range(3):
            plt3.plot(x, y[i], pen=(i, 3))  ## setting pen=(i,3) 自动创建3个不同颜色的笔
        self.gridLayout.addWidget(plt3, 2, 1, 1, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())