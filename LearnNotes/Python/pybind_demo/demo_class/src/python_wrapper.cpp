#include"add.h"
PYBIND11_MODULE(example, m)
{
	m.doc()="pybind11 example plugin";
	m.def("add", &add, "A function taht adds two numers", py::arg("i"), py::arg("j"));
	m.def("swap", [](py::buffer a, py::buffer b)\
	{   py::buffer_info a_info = a.request();
	    py::buffer_info b_info = b.request();
	    swap(static_cast<int *>(a_info.ptr), static_cast<int *>(b_info.ptr));
	});

    py::class_<Pet>(m, "Pet")
    .def(py::init<const std::string &>(), py::arg("name")="Dog")
    .def("setName", &Pet::setName)
    .def("getName", &Pet::getName);

    py::class_<Dog, Pet>(m, "Dog")
    .def(py::init<const std::string &>())
    .def("bark", &Dog::bark);
};


