cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(ITKDemo LANGUAGES CXX)

find_package(ITK REQUIRED)

add_executable(DicomSeriesReadNiftiImageWrite src/DicomSeriesReadNiftiImageWrite.cxx )
target_link_libraries(DicomSeriesReadNiftiImageWrite ${ITK_LIBRARIES})

add_executable(TwoProjectionRegistrationTestDriver 
					src/GetDRRSiddonJacobsRayTracing.cxx 
					src/TwoProjection2D3DRegistration.cxx 
					src/itkTwoProjectionImageRegistrationMethod.hxx
					src/itkTwoProjectionImageRegistrationMethod.h
					src/itkTwoImageToOneImageMetric.hxx
					src/itkTwoImageToOneImageMetric.h
					src/itkSiddonJacobsRayCastInterpolateImageFunction.hxx
					src/itkSiddonJacobsRayCastInterpolateImageFunction.h
					src/itkNormalizedCorrelationTwoImageToOneImageMetric.hxx
					src/itkNormalizedCorrelationTwoImageToOneImageMetric.h
					src/TwoProjectionRegistrationTestDriver.cxx )
target_link_libraries(TwoProjectionRegistrationTestDriver ${ITK_LIBRARIES})

add_executable(ReadResampleWriteNifti src/ReadResampleWriteNifti.cxx )
target_link_libraries(ReadResampleWriteNifti ${ITK_LIBRARIES})
