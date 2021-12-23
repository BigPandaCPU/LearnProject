from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

import pybind11

__version__ = "0.1"

ext_modules = [
	Pybind11Extension("python_example",
			["./example.cpp"],
			define_macros = [("VERSION_INFO", __version__)],
			),
]

setup(
	# name="test_example",
	# version=__version__,
	ext_modules = ext_modules,
	# cmdclass = {"build_ext":build_ext},
)