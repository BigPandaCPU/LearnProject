#!/usr/bin/env python

"""
=========================================================================

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/

"""
import pause
# First access the VTK module (and any other needed modules) by importing them.
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderer
)


def main(argv):
    colors = vtkNamedColors()

    #
    # The pipeline creation is documented in Tutorial_Step1.
    #
    cone = vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)

    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))
    axex_actor = vtkAxesActor()

    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.AddActor(axex_actor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))
    ren1.ResetCamera()

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Tutorial_Step2')

    # Here is where we setup the observer.
    mo1 = vtkMyCallback(ren1)
    ren1.AddObserver('StartEvent', mo1)
    renWin.Render()
    #
    # Now we loop over 360 degrees and render the cone each time.
    #
    for i in range(0, 360):
        # Render the image.
        #renWin.Render()
        #pause.seconds(0.1)
        # Rotate the active camera by one degree.
        ren1.GetActiveCamera().Azimuth(1)
    renWin.Render()

class vtkMyCallback(object):
    """
    Callback for the interaction.
    """

    def __init__(self, renderer):
        self.renderer = renderer

    def __call__(self, caller, ev):
        position = self.renderer.GetActiveCamera().GetPosition()
        print('({:5.2f}, {:5.2f}, {:5.2f})'.format(*position))


if __name__ == '__main__':
    import sys

    main(sys.argv)