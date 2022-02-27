from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import QGLWidget
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import *
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget


class vtkTimerCallback():
    def __init__(self):
        self.timer_count = 0

    def execute(self, obj, event):
        print(self.timer_count)
        self.actor.RotateY(self.timer_count % 360)
        self.actor.RotateX(self.timer_count % 360)
        self.actor.RotateZ(self.timer_count % 360)
        # self.actor.SetPosition(self.timer_count, self.timer_count, 0)
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1

class vtkMW(QMainWindow):
    """docstring for Mainwindow"""

    def __init__(self, parent=None):
        super(vtkMW, self).__init__(parent)
        self.basic()
        self.actor = vtk.vtkActor()
        vll = self.kuangti(self.actor)
        self.setCentralWidget(vll)
        # self.actor = vtk1.vtkActor()


    # 窗口基础属性
    def basic(self):
        # 设置标题，大小，图标
        self.setWindowTitle("vtkest5")
        self.resize(1100, 650)
        # self.setWindowIcon(QIcon("./image/Gt1.png"))

    def kuangti(self,actor):

        frame = QFrame()
        vl = QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor()
        vl.addWidget(vtkWidget)
        # vl.setContentsMargins(0,0,0,0)
        ren = vtk.vtkRenderer()
        ren.SetBackground(0.1, 0.2, 0.4)
        ren.SetBackground2(1.0, 1.0, 1.0)
        ren.SetGradientBackground(1)

        axes = vtk.vtkAxesActor()
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        widget = vtkOrientationMarkerWidget()
        widget.SetOutlineColor(0.9300, 0.5700, 0.1300)
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(renderWindowInteractor)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        widget.SetEnabled(1)
        widget.InteractiveOn()

        # vl.addWidget(renderWindowInteractor)
        # renderWindowInteractor.Start()
        # renderer.GetActiveCamera().SetPosition() #设置视点位置
        # renderer.GetActiveCamera().SetViewUp(0, 1, 0)  #设置视点方向
        vtkWidget.GetRenderWindow().AddRenderer(ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()
        self.Creatobj(ren,actor)
        self.iren.Initialize()
        frame.setLayout(vl)

        return frame

    def Creatobj(self, ren,actor):
        # Create source
        filename = "resource/FA-18.STL"
        reader = vtk.vtkSTLReader()
        # filename = "resource/flit6.obj"
        # reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)
        reader.Update()

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        # actor = vtk1.vtkActor()
        actor.SetMapper(mapper)
        # actor.RotateY(20 % 360)
        ren.AddActor(actor)
        ren.ResetCamera()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = vtkMW()
    win.show()
    # win.iren.Initialize()
    sys.exit(app.exec_())