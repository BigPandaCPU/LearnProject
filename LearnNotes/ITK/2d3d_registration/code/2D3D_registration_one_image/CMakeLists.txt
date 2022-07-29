cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(2D3DReg LANGUAGES CXX)
#set(ITK_DIR "D:/software/ITK_521/Debug/lib/cmake/ITK-5.2")
find_package(ITK REQUIRED)


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

