from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
__version__="0.0.1"
ext_modules=[
    Pybind11Extension(
        "DelaunayTriangulation",
        ["src/python_wrapper.cpp", "src/delaunay_triangulation.cpp"],
    ),
]

setup(
    name="DelaunayTriangulation",
    version=__version__,
    author="BigPanda",
    author_email="1196449387@qq.com",
    url="https://github.com/pybind/python_example",
    description="Delaunay Triangulation for 2d",
    long_description="",
    ext_modules=ext_modules,
    cmdclass={"build_ext":build_ext},
)