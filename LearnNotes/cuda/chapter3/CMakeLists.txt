cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(chapter3 LANGUAGES CXX CUDA)

add_executable(enum_gpu src/enum_gpu.cu common/book.h)
set_target_properties(enum_gpu PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
