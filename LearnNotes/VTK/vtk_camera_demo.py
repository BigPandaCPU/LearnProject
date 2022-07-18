from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2


def main():
    colors = vtkNamedColors()

    # Create a sphere
    # sphereSource = vtkCylinderSource()
    # sphereSource.SetCenter(0.0, 0.0, 0.0)
    # sphereSource.SetRadius(10)
    # sphereSource.SetPhiResolution(30)
    # sphereSource.SetThetaResolution(30)
    # sphereSource.Update()

    cylinderSource = vtkCylinderSource()
    cylinderSource.SetHeight(3.0)
    cylinderSource.SetRadius(1.0)
    cylinderSource.SetResolution(10)

    # Create a mapper and actor
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(cylinderSource.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetSpecular(0.6)
    actor.GetProperty().SetSpecularPower(30)
    actor.GetProperty().SetColor(colors.GetColor3d('LightSkyBlue'))

    camera = vtkCamera()
    camera.SetPosition(0, 0, 50)
    camera.SetFocalPoint(0, 0, 0)

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderer.SetActiveCamera(camera)

    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetWindowName('Camera')

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('MistyRose'))

    # Render and interact
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()