cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(chapter4 LANGUAGES CXX CUDA)

add_executable(test_add test.cu book.h)
set_target_properties(test_add PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
