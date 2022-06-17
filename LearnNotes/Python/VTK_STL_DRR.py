import itk
import vtk
import numpy as np

def augment_matrix_coord(array):
    n = len(array)
    return np.concatenate((array, np.ones((n,1))), axis = 1).T

def StlReader(StlModelFileName, import_mode = 'vtk'):
    """Function to read an stl file and returns it as a numpy array
        Args:
            stl_file_path
            import_mode (so fat only vtk)
    """
    if import_mode == 'vtk':
        # Load stl file
        readerSTL = vtk.vtkSTLReader()
        readerSTL.SetFileName(StlModelFileName)
        readerSTL.Update()

        polydata = readerSTL.GetOutput()

        # If there are no points in ''vtkPolyData' something went wrong
        if polydata.GetNumberOfPoints() == 0:
            raise ValueError("No point data could be loaded from" + StlModelFileName)
            return None

        return polydata


def MahfouzProjector(projector_info,
                    StlModelFileName,
                    PixelType,
                    correction_matrix = []):
    # ITK: Instantiate types
    Dimension = 2
    ImageType2D = itk.Image[PixelType, 2]
    RegionType = itk.ImageRegion[Dimension]
    moveImageInfo = {'Volume_center': (0.0, 0.0)}
    correction_matrix = correction_matrix

    # ITK: Set DRR image at initial position(at +focal length along the z direction)
    DRR = ImageType2D.New()
    DRRregion = RegionType()
    moveDirection = DRR.GetDirection()

    DRRstart = itk.Index[Dimension]()
    DRRstart.Fill(0)

    DRRsize = [0] * Dimension
    DRRsize[0] = projector_info['DRRsize_x']
    DRRsize[1] = projector_info['DRRsize_y']

    DRRregion.SetSize(DRRsize)
    DRRregion.SetIndex(DRRstart)

    DRRspacing = itk.Point[itk.F, Dimension]()
    DRRspacing[0] = projector_info['DRRspacing_x']
    DRRspacing[1] = projector_info['DRRspacing_y']

    DRRorigin = itk.Point[itk.F, Dimension]()
    DRRorigin[0] = moveImageInfo['Volume_center'][0] - projector_info['DRR_ppx'] - DRRspacing[0] * (
                DRRsize[0] - 1.) / 2.0
    DRRorigin[1] = moveImageInfo['Volume_center'][1] - projector_info['DRR_ppy'] - DRRspacing[1] * (
                DRRsize[1] - 1.) / 2.0

    DRR.SetRegions(DRRregion)
    DRR.Allocate()
    DRR.SetSpacing(DRRspacing)
    DRR.SetOrigin(DRRorigin)
    moveDirection.SetIdentity()
    DRR.SetDirection(moveDirection)

    # Load stl mesh (with vtk function)
    StlMesh = StlReader(StlModelFileName)

    # the correction matrix allows to make the local CS of the object coincidde with the standard camera CS
    # if correction_matrix:
    #     StlPoints = np.dot(correction_matrix, augment_matrix_coord(StlPoints))[0:3].T

    # Set Camera parameters (conver from mm to pixel units)
    ppx_pixels = projector_info['DRR_ppx'] / DRRspacing[0]
    ppy_pixels = projector_info['DRR_ppy'] / DRRspacing[1]
    focal_length_pixels = projector_info['focal_lenght'] / DRRspacing[0]
    near = projector_info['near']
    far = projector_info['far']

    # Prepare Gaussian filters for intensity image
    IntGaussSigma = projector_info['intGsigma']
    IntGaussSize = projector_info['intGsize']

    # VTK:Initialize first rendering
    # Mapper
    init_mapper = vtk.vtkPolyDataMapper()
    init_mapper.SetInputData(StlMesh)

    # Actor for binary image
    actor = vtk.vtkActor()
    actor.SetMapper(init_mapper)
    actor.GetProperty().SetColor(0.0, 0.0, 0.0)
    actor.GetProperty().SetAmbient(1)
    actor.GetProperty().SetDiffuse(0)

    axes = vtk.vtkAxesActor()

    # Renderer for binary image
    MahfouzRenderer = vtk.vtkRenderer()
    MahfouzRenderer.AddActor(actor)
    MahfouzRenderer.SetBackground(1, 1, 1)

    MahfouzRenderer.AddActor(axes)

    # Renderer window
    MahfouzRenderWindow = vtk.vtkRenderWindow()
    MahfouzRenderWindow.AddRenderer(MahfouzRenderer)
    ##MahfouzRenderWindow.SetOffScreenRendering(1)  # it prevents generating a window
    MahfouzRenderWindow.SetSize(DRRsize[0], DRRsize[1])
    #MahfouzRenderWindow.Render()

    # Camera parameters
    Camera = MahfouzRenderer.GetActiveCamera()
    Camera.SetClippingRange(near, far)
    Camera.SetPosition(0, 0, 0)
    Camera.SetFocalPoint(0, 0, -1)
    Camera.SetViewUp(0, 1, 0)

    # Set window center for offset principal point
    # if principal point is referred to principal ray
    wcx = -2.0 * (ppx_pixels) / DRRsize[0]
    wcy = -2.0 * (ppy_pixels) / DRRsize[1]

    Camera.SetWindowCenter(wcx, wcy)

    angle = 180.0 / np.pi * 2.0 * np.arctan2(DRRsize[1] / 2.0, focal_length_pixels)
    Camera.SetViewAngle(angle)

    MahfouzRenderWindow.Render()
    MahfouzRenderer.ResetCamera()


    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(MahfouzRenderWindow)
    iren.Initialize()
    MahfouzRenderWindow.Render()
    iren.Start()

    # Initial Window to image filter
    # init_windowToImageFilter = vtk.vtkWindowToImageFilter()
    # init_windowToImageFilter.SetInput(MahfouzRenderWindow)
    # init_windowToImageFilter.Update()


if __name__=="__main__":

    CameraParamFilepath = "./HOPE_Test_camera_intrinsic_parameters.txt"
    StlModelFileName = "./HOPE_Test_Stem.stl"
    PixelType = itk.F
    Dimension = 3
    ScalarType = itk.D

    Projector_info = {'Name': 'Mahfouz',
                      'near': 0.1,
                      'far': 3000,
                      'intGsigma': 2,
                      'intGsize': (5, 5),
                      '3Dmodel': 'Stem'}

    intrinsic_parameters = np.genfromtxt(CameraParamFilepath, delimiter=',', usecols=[1])
    Projector_info['focal_lenght'] = intrinsic_parameters[0]
    Projector_info['DRRspacing_x'] = intrinsic_parameters[1]
    Projector_info['DRRspacing_y'] = intrinsic_parameters[2]
    Projector_info['DRR_ppx'] = intrinsic_parameters[3]
    Projector_info['DRR_ppy'] = intrinsic_parameters[4]
    Projector_info['DRRsize_x'] = int(intrinsic_parameters[5])
    Projector_info['DRRsize_y'] = int(intrinsic_parameters[6])
    Projector_info['threadsPerBlock_x'] = 16
    Projector_info['threadsPerBlock_y'] = 16


    MahfouzProjector(Projector_info,StlModelFileName,PixelType,ScalarType)



# import itk
# Dimension = 2
# SizeType = itk.Size[Dimension]
# size = SizeType()
# size.Fill(3)
# IndexType = itk.Index[Dimension]
# start = IndexType()
# start[0] = 2
# start[1] = 2
#
# RegionType = itk.ImageRegion[Dimension]
# region = RegionType(start, size)
#
# testPixel1 = IndexType()
# testPixel1[0] = 1
# testPixel1[1] = 1
#
# testPixel2 = IndexType()
# testPixel2[0] = 4
# testPixel2[1] = 5
#
# print(testPixel1, end=" ")
# if region.IsInside(testPixel1):
#     print("Inside")
# else:
#     print("Outside")