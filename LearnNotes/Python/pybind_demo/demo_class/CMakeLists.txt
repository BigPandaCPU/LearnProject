cmake_minimum_required(VERSION 2.8.12)
project(example)
find_package(pybind11 REQUIRED)
include_directories(${pybind11_INCLUDE_DIRS})

pybind11_add_module(example
    src/add.cpp
    src/add.h
    src/python_wrapper.cpp
    )

