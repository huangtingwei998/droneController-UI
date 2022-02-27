from __future__ import print_function

import vtk
from vtk.qt.QVTKRenderWindowInteractor import *
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget


class vtkTimerCallback11():
    def __init__(self,transform):
        self.timer_count = 10
        self.actor = transform

    def execute(self, obj, event):
        print(self.timer_count)
        # self.actor.RotateY(self.timer_count % 360)
        # self.actor.RotateX(self.timer_count % 360)
        self.actor.RotateZ(self.timer_count % 360)
        iren = obj
        iren.GetRenderWindow().Render()



def main():
    # 创建一个球体
    # cubeSource = vtk1.vtkCubeSource()
    # cubeSource = vtk1.vtkCylinderSource()
    # cubeSource.SetCenter(0.0, 0.0, 0.0)
    # 加载STL文件
    # filename = "resource/FA-18.STL"
    # reader = vtk.vtkSTLReader()
    # 加载obj文件
    filename = "resource/flit6.obj"
    reader = vtk.vtkOBJReader()
    reader.SetFileName(filename)
    reader.Update()
    # 创建mapper和actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(0.1, 0.2, 0.4)
    # prop = actor.GetProperty()

    # Setup a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.2, 0)
    renderer.SetBackground2(0.8, 0.9, 1.0)
    renderer.SetGradientBackground(1)


    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Test")
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)  # Background color white

    # Render and interact
    renderWindow.Render()

    # 必须在创建计时器事件之前需初始化
    renderWindowInteractor.Initialize()

    axes = vtk.vtkAxesActor()

    # axes.SetMapper(mapper)
    widget = vtkOrientationMarkerWidget()
    widget.SetOutlineColor(0.9300, 0.5700, 0.1300)
    widget.SetOrientationMarker(axes)
    widget.SetInteractor(renderWindowInteractor)
    widget.SetViewport(0.0, 0.0, 0.4, 0.4)
    widget.SetEnabled(1)
    widget.InteractiveOn()

    transform = vtkTransform()
    actor.SetUserTransform(transform)
    axes.SetUserTransform(transform)

    # 注册计时器时事件
    cb = vtkTimerCallback11(transform)

    renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
    renderWindowInteractor.CreateRepeatingTimer(40)



    # start the interaction and timer
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
    timew = vtkTimerCallback11()