#include"add.h"
PYBIND11_MODULE(example, m)
{
	m.doc()="pybind11 example plugin";
	m.def("add", &add, "A function taht adds two numers", py::arg("i"), py::arg("j"));
}
