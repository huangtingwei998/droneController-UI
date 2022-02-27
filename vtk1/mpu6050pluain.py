import qdarkstyle
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import QGLWidget
import sys
import vtk
from vtktest5 import vtkMW
from myserial.grapy import mpu6050plot


class MainWindow(QMainWindow):
    """docstring for Mainwindow"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.basic()
        splitter_main = self.split_()
        self.setCentralWidget(splitter_main)

        # 窗口基础属性

    def basic(self):
        # 设置标题，大小，图标
        self.setWindowTitle("GT")
        self.resize(1100, 650)
        self.setWindowIcon(QIcon("./image/Gt.png"))
        # 居中显示
        screen = QDesktopWidget().geometry()
        self_size = self.geometry()
        self.move((screen.width() - self_size.width()) / 2, (screen.height() - self_size.height()) / 2)

        # 分割窗口

    def split_(self):
        vl = QVBoxLayout()
        vtkWidget = vtkMW()
        vl.addWidget(vtkWidget)
        mpuplot = mpu6050plot()
        vl.addWidget(mpuplot)
        splitter_main = QSplitter(Qt.Horizontal)
        splitter_main.addWidget(vtkWidget)
        splitter_main.addWidget(mpuplot)
        return splitter_main




if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()
    # win.iren.Initialize()
    sys.exit(app.exec_())
