import itk
ImageType = itk.Image[itk.F, 3]
registration_method = itk.TwoProjectionImageRegistrationMethod[ImageType, ImageType].New()