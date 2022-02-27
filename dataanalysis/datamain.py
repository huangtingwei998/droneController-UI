# gridlayout2.py
from PyQt5.QtWidgets import QApplication, QLineEdit, QLabel, QGridLayout
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import dataanalysis.pie


class GridLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setWindowTitle('grid layout')


        self.browser = QWebEngineView()
        self.browser2 = QWebEngineView()
        self.browser3 = QWebEngineView()
        self.browser4 = QWebEngineView()
        self.browser.load(QUrl('C:/Users/huangtingwei/Desktop/飞行器pythonProject17/dataanalysis/html/Bing1.html'))


        self.browser2.load(QUrl('C:/Users/huangtingwei/Desktop/飞行器pythonProject17/dataanalysis/html/bar.html'))

        self.browser3.load(QUrl('C:/Users/huangtingwei/Desktop/飞行器pythonProject17/dataanalysis/html/line.html'))
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.browser, 1, 0)
        grid.addWidget(self.browser2, 1, 1)
        grid.addWidget(self.browser3, 2, 0)
        grid.addWidget(self.browser4, 2, 1)

        self.setLayout(grid)
        self.resize(1600, 1200)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    qb = GridLayout()
    qb.show()
    sys.exit(app.exec_())
