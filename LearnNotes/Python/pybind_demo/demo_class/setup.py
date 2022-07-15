from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
__version__="0.0.1"
ext_modules=[
    Pybind11Extension(
        "example",
        ["src/python_wrapper.cpp", "src/add.cpp"],
    ),
]

setup(
    name="example",
    version=__version__,
    author="Sylvain Corlay",
    author_email="sylvain.corlay@gmail.com",
    url="https://github.com/pybind/python_example",
    description="A test project using pybind11",
    long_description="",
    ext_modules=ext_modules,
    cmdclass={"build_ext":build_ext},
)