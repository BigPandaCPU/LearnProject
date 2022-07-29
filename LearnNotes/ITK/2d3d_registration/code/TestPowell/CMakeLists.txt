cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(ITKDemo LANGUAGES CXX)
set(ITK_DIR "D:/software/ITK_521/Debug/lib/cmake/ITK-5.2")
find_package(ITK REQUIRED)

add_executable(testPowell src/test_powell.cpp )
target_link_libraries(testPowell ${ITK_LIBRARIES})
