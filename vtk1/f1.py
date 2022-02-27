#!/usr/bin/env python
import sys
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QApplication, QLineEdit, QToolBar, QLabel, QHBoxLayout, \
    QSlider
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.util.colors import light_grey

filenames = ["resource/Drone-Tla.STL"]

dt = 1.0  # 最小的旋转计量单位
angle = [0, 0]  # shoulder and elbow joint angle

# renWin = vtk.vtkRenderWindow()
assembly = vtk.vtkAssembly()
slider_X = vtk.vtkSliderRepresentation2D()
slider_Y = vtk.vtkSliderRepresentation2D()
slider_Z = vtk.vtkSliderRepresentation2D()
actor = list()  # the list of links

class VTKWindow(QMainWindow):
    """docstring for Mainwindow"""

    def __init__(self, parent=None):
        super(VTKWindow, self).__init__(parent)
        self.setWindowTitle("vtkest5")
        # self.ser = serial.Serial('COM4', 115200, timeout=5)
        self.timer = QTimer()
        self.timer.timeout.connect(self.data_receive)
        self.timer.start(20)
        # self.ser.flushInput()


        hayout = QHBoxLayout()
        layout = QVBoxLayout()

        self.s1 = QSlider(Qt.Horizontal)
        ##设置最小值
        self.s1.setMinimum(0)
        # 设置最大值
        self.s1.setMaximum(360)
        # 步长
        self.s1.setSingleStep(1)
        # 设置当前值
        self.s1.setValue(0)
        self.s1.valueChanged.connect(self.getdata)
        self.s2 = QSlider(Qt.Horizontal)
        ##设置最小值
        self.s2.setMinimum(0)
        # 设置最大值
        self.s2.setMaximum(360)
        # 步长
        self.s2.setSingleStep(1)
        # 设置当前值
        self.s2.setValue(0)
        self.s2.valueChanged.connect(self.getdata)
        self.s3 = QSlider(Qt.Horizontal)
        ##设置最小值
        self.s3.setMinimum(0)
        # 设置最大值
        self.s3.setMaximum(360)
        # 步长
        self.s3.setSingleStep(1)
        # 设置当前值
        self.s3.setValue(0)
        self.s3.valueChanged.connect(self.getdata)
        hayout.addWidget(self.s1)
        hayout.addWidget(self.s2)
        hayout.addWidget(self.s3)



        self.actor = list()
        self.vll =self.CreateScene(self.actor)
        layout.addWidget(self.vll)

        self.setCentralWidget(self.vll)
        self.resize(1100, 650)
        navigation_bar = QToolBar('Navigation')

        self.xdata = QLineEdit()
        self.xdata.returnPressed.connect(self.getdata)
        self.ydata = QLineEdit()
        self.ydata.returnPressed.connect(self.getdata)
        self.zdata = QLineEdit()
        self.zdata.returnPressed.connect(self.getdata)
        self.xtext = QLabel("x轴数据")
        self.ytext = QLabel("y轴数据")
        self.ztext = QLabel("z轴数据")
        self.addToolBar(navigation_bar)
        navigation_bar.addWidget(self.xtext)
        navigation_bar.addWidget(self.xdata)
        navigation_bar.addWidget(self.ytext)
        navigation_bar.addWidget(self.ydata)
        navigation_bar.addWidget(self.ztext)
        navigation_bar.addWidget(self.zdata)
        navigation_bar.addWidget(self.s1)
        navigation_bar.addWidget(self.s2)
        navigation_bar.addWidget(self.s3)

    def getdata(self):

        xdat = self.s1.value()
        ydat = self.s2.value()
        zdat = self.s3.value()
        xdat = int(xdat)
        ydat = int(ydat)
        zdat = int(zdat)
        self.xdata.setText(str(xdat))
        self.ydata.setText(str(ydat))
        self.zdata.setText(str(zdat))
        self.changeview(xdat, ydat, zdat)

    def changeview(self,xdat, ydat, zdat):
        self.actor[0].SetOrientation(xdat, ydat, zdat)
        self.actor[0].RotateX(90)
        self.iren.GetRenderWindow().Render()

    def XSliderCallback(self,obj, event):
        x, y, z = self.getdata()
        actor[0].SetOrientation(-x, -y, -z)
        actor[0].RotateX(90)

    def CreateScene(self,actor):
        frame = QFrame()
        self.ren = vtk.vtkRenderer()
        vl = QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor()
        vl.addWidget(vtkWidget)
        vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = vtkWidget.GetRenderWindow().GetInteractor()


        for id, file in enumerate(filenames):
            actor.append(LoadSTL(file))
            # actor[id].GetProperty().SetColor(blue)
            r = vtk.vtkMath.Random(.4, 1.0)
            g = vtk.vtkMath.Random(.4, 1.0)
            b = vtk.vtkMath.Random(.4, 1.0)
            actor[id].GetProperty().SetDiffuseColor(r, g, b)
            actor[id].GetProperty().SetDiffuse(.8)
            actor[id].GetProperty().SetSpecular(.5)
            actor[id].GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
            actor[id].GetProperty().SetSpecularPower(30.0)


        # 设置旋转原点

        actor[0].SetOrigin(243, 100, 243)
        actor[0].RotateX(90)
        self.ren.AddActor(actor[0])

        # 创建坐标
        axes = CreateCoordinates()
        self.ren.AddActor(axes)

        # 背景
        ground = CreateGround()
        self.ren.AddActor(ground)
        self.ren.SetBackground(.2, .2, .2)

        # 创建相机并设定相机视角
        camera = vtk.vtkCamera()
        camera.SetFocalPoint(200, 0, 0)
        camera.SetPosition(200, -450, 250)
        camera.ComputeViewPlaneNormal()
        camera.SetViewUp(0, 1, 0)
        camera.Zoom(0.4)
        self.ren.SetActiveCamera(camera)

        # Enable user interface interactor
        self.iren.Initialize()
        self.iren.Start()
        # return renWin
        frame.setLayout(vl)
        return frame


    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num).decode('utf-8')
            data = data.rstrip('\n').split('\t')
            x = int(float(data[0]))
            y = int(float(data[1]))
            z = int(float(data[2].split('\n')[0]))
            print(x,y,z)
            self.changeview(x,-y,z)
        else:
            pass

    def port_close(self):
        self.timer.stop()
        try:
            self.ser.close()
        except:
            pass


#    加载STL文件
def LoadSTL(filename):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    mapper = vtk.vtkPolyDataMapper()  # maps polygonal data to graphics primitives
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtk.vtkLODActor()
    actor.SetMapper(mapper)
    return actor  # represents an entity in a rendered scene

# 建立坐标
def CreateCoordinates():
    # create coordinate axes in the render window
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(100, 100, 100)  # Set the total length of the axes in 3 dimensions

    # Set the type of the shaft to a cylinder:0, line:1, or user defined geometry.
    axes.SetShaftType(0)

    axes.SetCylinderRadius(0.02)
    axes.GetXAxisCaptionActor2D().SetWidth(0.03)
    axes.GetYAxisCaptionActor2D().SetWidth(0.03)
    axes.GetZAxisCaptionActor2D().SetWidth(0.03)
    # axes.SetAxisLabels(0)  # Enable:1/disable:0 drawing the axis labels
    # transform = vtk.vtkTransform()
    # transform.Translate(0.0, 0.0, 0.0)
    # axes.SetUserTransform(transform)
    # axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(1,0,0)
    # axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().BoldOff() # disable text bolding
    return axes


def XSliderCallback(obj, event):
    x,y,z = VTKWindow.getdata()
    actor[0].SetOrientation(-x, -y, -z)
    actor[0].RotateX(90)


def YSliderCallback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    actor[0].SetOrientation(0, -pos, 0)
    actor[0].RotateX(90)


def ZSliderCallback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    actor[0].SetOrientation(0, 0, -pos)
    actor[0].RotateX(90)





def ConfigSlider(sliderRep, TitleText, Yaxes):
    sliderRep.SetMinimumValue(0.0)
    sliderRep.SetMaximumValue(360.0)
    sliderRep.SetValue(0.0)  # Specify the current value for the widget
    sliderRep.SetTitleText(TitleText)  # Specify the label text for this widget

    sliderRep.GetSliderProperty().SetColor(1, 0, 0)  # Change the color of the knob that slides
    sliderRep.GetSelectedProperty().SetColor(0, 0, 1)  # Change the color of the knob when the mouse is held on it
    sliderRep.GetTubeProperty().SetColor(1, 1, 0)  # Change the color of the bar
    sliderRep.GetCapProperty().SetColor(0, 1, 1)  # Change the color of the ends of the bar
    # sliderRep.GetTitleProperty().SetColor(1,0,0)  # Change the color of the text displaying the value

    # Position the first end point of the slider
    sliderRep.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
    sliderRep.GetPoint1Coordinate().SetValue(50, Yaxes)

    # Position the second end point of the slider
    sliderRep.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
    sliderRep.GetPoint2Coordinate().SetValue(400, Yaxes)

    sliderRep.SetSliderLength(0.02)  # Specify the length of the slider shape.The slider length by default is 0.05
    sliderRep.SetSliderWidth(0.02)  # Set the width of the slider in the directions orthogonal to the slider axis
    sliderRep.SetTubeWidth(0.005)
    sliderRep.SetEndCapWidth(0.03)

    sliderRep.ShowSliderLabelOn()  # display the slider text label
    sliderRep.SetLabelFormat("%.1f")

    sliderWidget = vtk.vtkSliderWidget()
    sliderWidget.SetRepresentation(sliderRep)
    sliderWidget.SetAnimationModeToAnimate()

    return sliderWidget


def CreateGround():
    # create plane source
    plane = vtk.vtkPlaneSource()
    plane.SetXResolution(50)
    plane.SetYResolution(50)
    plane.SetCenter(0, 0, 0)
    plane.SetNormal(0, 0, 1)

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetRepresentationToWireframe()
    # actor.GetProperty().SetOpacity(0.4)  # 1.0 is totally opaque and 0.0 is completely transparent
    actor.GetProperty().SetColor(light_grey)

    '''
    # Load in the texture map. A texture is any unsigned char image.
    bmpReader = vtk.vtkBMPReader()  
    bmpReader.SetFileName("ground_texture.bmp")  
    texture = vtk.vtkTexture()  
    texture.SetInputConnection(bmpReader.GetOutputPort())  
    texture.InterpolateOn()  
    actor.SetTexture(texture)
    '''
    transform = vtk.vtkTransform()
    transform.Scale(2000, 2000, 1)
    actor.SetUserTransform(transform)

    return actor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VTKWindow()
    win.show()
    sys.exit(app.exec_())
    # CreateScene()