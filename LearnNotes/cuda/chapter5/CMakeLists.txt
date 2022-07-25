cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(chapter5 LANGUAGES CXX CUDA)
set(OpenCV_DIR "D:/software/opencv/build")
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBRARY_DIRS})

add_executable(ripple src/ripple.cu common/book.h)
set_target_properties(ripple PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
target_link_libraries(ripple ${OpenCV_LIBRARIES})


add_executable(dot src/dot.cu common/book.h)
set_target_properties(dot PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
target_link_libraries(dot ${OpenCV_LIBRARIES})