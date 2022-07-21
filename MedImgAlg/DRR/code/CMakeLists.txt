project(SiddonGpu)

find_package(CUDA REQUIRED)
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

cuda_add_library(SiddonGpu SiddonLib/siddon_class.cu SiddonLib/siddon_class.cuh)
target_link_libraries(SiddonGpu cudart cudadevrt)
ADD_EXECUTABLE(main SiddonLib/test.cxx)
target_link_libraries(main SiddonGpu ${ITK_LIBRARIES})