import itk
import vtk

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

        polydata = readerSTL.GetOuput()

        # If there are no points in ''vtkPolyData' something went wrong
        if polydata.GetNumberOfPoints() == 0:
            raise ValueError("No point data could be loaded from" + StlModelFileName)
            return None

        return polydata

class Mahfouz():
    """Binary DRR generation from STL model.
        this class renders a binary image using VTK and smooths it with
        Gaussian filter using OpenCV:

        Methods:
            _new_rendoer(function):sets up a new rendoer for a new DRR
            compute(function):returns a 2D image(DRR) as a numpy array.
            delete(function):eventually deletes the projector obejct(only
            needed to deallocate memory from GPU)

        Note:the camera coordinate system has the y axis pointing downwards

    """
    def __init__(self, projector_info,
                    StlModelFileName,
                    PixelType,
                    Dimension,
                    ScalarType,
                    correction_matrix = []):
        """Prepares itk stuff, loads stl and initializes VTK render.

            Args:
                projector_info(dict ot str):with the following keys:
                - Name:'Mahfouz'
                - near (float):near clipping plane(vtk)
                - far (float):far clipping plane(vtk)
                - intGSigma (int):sigma of the Haussian filter
                - intGSize (int):size of the Gaussian kernal
                - 3Dmodel (str): name of 3D model (ie. stem)
        """

        #ITK: Instantiate types
        self.Dimension = 2
        self.ImageType2D = itk.Image[PixelType, 2]
        self.RegionType = itk.ImageRegion[self.Dimension]
        moveImageInfo = {'Volume_center':(0.0, 0.0)}
        self.correction_matrix = correction_matrix

        #ITK: Set DRR image at initial position(at +focal length along the z direction)
        DRR = self.ImageType2D.New()
        self.DRRregion = self.RegionType()
        self.moveDirection = DRR.GetDirection()

        DRRstart = itk.Index[self.Dimension]()
        DRRstart.Fill(0)

        self.DRRsize = [0]*self.Dimension
        self.DRRsize[0] = projector_info['DRRsize_x']
        self.DRRsize[1] = projector_info['DRRsize_y']

        self.DRRregion.SetSize(self.DRRsize)
        self.DRRregion.SetIndex(DRRstart)

        self.DRRspacing = itk.Point[itk.F, self.Dimension]
        self.DRRspacing[0] = projector_info['DRRspacing_x']
        self.DRRspacing[1] = projector_info['DRRspacing_y']

        self.DRRorigin = itk.Point[itk.F, self.Dimension]
        self.DRRorigin[0] = moveImageInfo['Volume_center'][0] - projector_info['DRR_ppx'] - self.DRRspacing[0]*(self.DRRsize[0] - 1.) / 2.0
        self.DRRorigin[1] = moveImageInfo['Volume_center'][1] - projector_info['DRR_ppy'] - self.DRRspacing[1]*(self.DRRsize[1] - 1.) / 2.0

        DRR.SetRegion(self.DRRregion)
        DRR.Allocate()
        DRR.SetSpacing(self.DRRspacing)
        DRR.SetOrigin(self.DRRorigin)
        self.moveDirection.SetIdentity()
        DRR.SetDirection(self.moveDirection)

        # Load stl mesh (with vtk function)
        self.StlMesh = StlReader(StlModelFileName)

        #the correction matrix allows to make the local CS of the object coincidde with the standard camera CS
        if self.correction_matrix:
            self.StlPoints = np.dot(correction_matrix, augment_matrix_coord(StlPoints))[0:3].T

        #Set Camera parameters (conver from mm to pixel units)
        self.ppx_pixels = projector_info['DRR_ppx']/self.DRRspacing[0]
        self.ppy_pixels = projector_info['DRR_ppy']/self.DRRspacing[1]
        self.focal_length_pixels = projector_info['focal_lenght']/self.DRRspacing[0]
        self.near = projector_info['near']
        self.far = projector_info['far']


        #Prepare Gaussian filters for intensity image
        self.IntGaussSigma = projector_info['intGsigma']
        self.IntGaussSize = projector_info['intGsize']

        #VTK:Initialize first rendering
        #Mapper
        init_mapper = vtk.vtkPolyDataMapper()
        init_mapper.SetInputData(self.StlMesh)

        #Actor for binary image
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(init_mapper)
        self.actor.GetProperty().SetColor(0.0, 0.0, 0.0)
        self.actor.GetProperty().SetAmbient(1)
        self.actor.GetProperty().SetDiffuse(0)

        # Renderer for binary image
        self.MahfouzRenderer = vtk.vtkRenderer()
        self.MahfouzRenderer.AddActor(self.actor)
        self.MahfouzRenderer.SetBackground(1, 1, 1)

        #Renderer window
        self.MahfouzRenderWindow = vtk.vtkRenderWindow()
        self.MahfouzRenderWindow.AddRenderer(self.MahfouzRenderer)
        self.MahfouzRenderWindow.SetOffScreenRendering(1) #it prevents generating a window
        self.MahfouzRenderWindow.SetSize(self.DRRsize[0], self.DRRsize[1])
        self.MahfouzRenderWindow.Render()

        #Camera parameters
        self.Camera = self.MahfouzRenderer.GetActiveCamera()
        self.Camera.SetClippingRange(self.near, self.far)
        self.Camera.SetPosition(0, 0, 0)
        self.Camera.SetFocalPoint(0, 0,-1)
        self.Camera.SetViewUp(0, 1, 0)

        #Set window center for offset principal point
        # if principal point is referred to principal ray
        wcx = -2.0*(self.ppx_pixels)/self.DRRsize[0]
        wcy = -2.0*(self.ppy_pixels)/self.DRRsize[1]

        self.Camera.SetWindowCenter(wcx, wcy)

        angle = 180.0/np.pi*2.0*np.arctan2(self.DRRsize[1] / 2.0, self.focal_length_pixels)
        self.Camera.SetViewAngle(angle)

        self.MahfouzRenderWindow.Render()

        # Initial Window to image filter
        init_windowToImageFilter = vtk.vtkWindowToImageFilter()
        init_windowToImageFilter.SetInput(self.MahfouzRenderWindow)
        init_windowToImageFilter.Update()


import itk
Dimension = 2
SizeType = itk.Size[Dimension]
size = SizeType()
size.Fill(3)
IndexType = itk.Index[Dimension]
start = IndexType()
start[0] = 2
start[1] = 2

RegionType = itk.ImageRegion[Dimension]
region = RegionType(start, size)

testPixel1 = IndexType()
testPixel1[0] = 1
testPixel1[1] = 1

testPixel2 = IndexType()
testPixel2[0] = 4
testPixel2[1] = 5

print(testPixel1, end=" ")
if region.IsInside(testPixel1):
    print("Inside")
else:
    print("Outside")