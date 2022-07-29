cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(chapter6 LANGUAGES CXX CUDA)
set(OpenCV_DIR "D:/software/opencv/build")
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBRARY_DIRS})

add_executable(ray_noconst src/ray_noconst.cu common/book.h)
set_target_properties(ray_noconst PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
target_link_libraries(ray_noconst ${OpenCV_LIBRARIES})

add_executable(ray_const src/ray.cu common/book.h)
set_target_properties(ray_const PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
target_link_libraries(ray_const ${OpenCV_LIBRARIES})
