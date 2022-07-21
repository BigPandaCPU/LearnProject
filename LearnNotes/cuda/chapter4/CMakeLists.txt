cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(chapter4 LANGUAGES CXX CUDA)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBRARY_DIRS})

add_executable(test_add src/test.cu common/book.h)
set_target_properties(test_add PROPERTIES CUDA_SEPARABLE_COMPILATION ON)

add_executable(julia_cpu src/julia_cpu.cu common/image.h)
set_target_properties(julia_cpu PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
target_link_libraries(julia_cpu ${OpenCV_LIBRARIES})

add_executable(julia_gpu src/julia_gpu.cu common/image.h common/book.h)
set_target_properties(julia_gpu PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
target_link_libraries(julia_gpu ${OpenCV_LIBRARIES})