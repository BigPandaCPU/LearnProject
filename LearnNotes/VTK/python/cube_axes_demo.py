#!/usr/bin/env python
# 了解相机的6个关键参数，以superquadric超二次曲面为例
# focalpoint 焦点，默认是坐标原点(0, 0, 0)
# position  相机位置，默认是(0, 0, 1)
# viewUp 默认是Y轴，为上方向.(0, 1, 0)
# roll: 垂直于投影方向进行旋转
# Azimuth: 水平方向旋转
# Elevation：上下旋转


# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    backgroundColor = colors.GetColor3d("DarkSlateGray")
    actorColor = colors.GetColor3d("Tomato")
    axis1Color = colors.GetColor3d("Salmon")
    axis2Color = colors.GetColor3d("PaleGreen")
    axis3Color = colors.GetColor3d("LightSkyBlue")

    # Create a superquadric
    superquadricSource = vtkSuperquadricSource()
    superquadricSource.SetPhiRoundness(3.1)
    superquadricSource.SetThetaRoundness(1.0)
    superquadricSource.Update()  # needed to GetBounds later

    renderer = vtkRenderer()

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(superquadricSource.GetOutputPort())

    superquadricActor = vtkActor()
    superquadricActor.SetMapper(mapper)
    superquadricActor.GetProperty().SetDiffuseColor(actorColor)
    superquadricActor.GetProperty().SetDiffuse(.7)
    superquadricActor.GetProperty().SetSpecular(.7)
    superquadricActor.GetProperty().SetSpecularPower(50.0)

    cubeAxesActor = vtkCubeAxesActor()
    cubeAxesActor.SetUseTextActor3D(1)
    cubeAxesActor.SetBounds(superquadricSource.GetOutput().GetBounds())
    cubeAxesActor.SetCamera(renderer.GetActiveCamera())
    cubeAxesActor.GetTitleTextProperty(0).SetColor(axis1Color)
    cubeAxesActor.GetTitleTextProperty(0).SetFontSize(48)
    cubeAxesActor.GetLabelTextProperty(0).SetColor(axis1Color)

    cubeAxesActor.GetTitleTextProperty(1).SetColor(axis2Color)
    cubeAxesActor.GetLabelTextProperty(1).SetColor(axis2Color)

    cubeAxesActor.GetTitleTextProperty(2).SetColor(axis3Color)
    cubeAxesActor.GetLabelTextProperty(2).SetColor(axis3Color)

    cubeAxesActor.DrawXGridlinesOn()
    cubeAxesActor.DrawYGridlinesOn()
    cubeAxesActor.DrawZGridlinesOn()
    cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)

    cubeAxesActor.XAxisMinorTickVisibilityOff()
    cubeAxesActor.YAxisMinorTickVisibilityOff()
    cubeAxesActor.ZAxisMinorTickVisibilityOff()

    cubeAxesActor.SetFlyModeToStaticEdges()
    renderer.AddActor(cubeAxesActor)
    renderer.AddActor(superquadricActor)
    camera = renderer.GetActiveCamera()
    focalPoint = camera.GetFocalPoint()
    pos = camera.GetPosition()
    viewUp = camera.GetViewUp()
    dis = camera.GetDistance()

    print("focalPoint:", focalPoint)
    print("position:", pos)
    print("viewUp:", viewUp)
    print("distance:", dis)

    #camera.SetViewUp(1, 0, 0)
    #camera.SetFocalPoint(1,1,1)
    camera.SetPosition(0,1,0)
    #camera.Elevation(90) #上下旋转
    #camera.Roll(30)  #与投影方向垂直的平面上旋转
    #camera.Azimuthe(30) #水平方向旋转

    # renderer.GetActiveCamera().Azimuth(30)
    # renderer.GetActiveCamera().Elevation(30)
    #renderer.GetActiveCamera().SetFocalPoint(1,0,0)


    renderer.ResetCamera()  #自动调整相机参数（应该是距离远近），使得将整个图像显示在窗口中
    renderer.SetBackground(backgroundColor)

    renderWindow = vtkRenderWindow()

    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(640, 480)
    renderWindow.SetWindowName('CubeAxesActor')

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renderer.GetActiveCamera().Zoom(0.8)
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()