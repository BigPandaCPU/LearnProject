#include<iostream>
#include<pybind11/pybind11.h>
#include<pybind11/numpy.h>

namespace py = pybind11;

/*
1d矩阵相加
*/
py::array_t<double> add_arrays_1d(py::array_t<double>& input1, py::array_t<double>& input2) {

    // 获取input1, input2的信息
    py::buffer_info buf1 = input1.request();
    py::buffer_info buf2 = input2.request();

    if (buf1.ndim !=1 || buf2.ndim !=1)
    {
        throw std::runtime_error("Number of dimensions must be one");
    }

    if (buf1.size !=buf2.size)
    {
        throw std::runtime_error("Input shape must match");
    }

    //申请空间
    auto result = py::array_t<double>(buf1.size);
    py::buffer_info buf3 = result.request();

    //获取numpy.ndarray 数据指针
    double* ptr1 = (double*)buf1.ptr;
    double* ptr2 = (double*)buf2.ptr;
    double* ptr3 = (double*)buf3.ptr;

    //指针访问numpy.ndarray
    for (int i = 0; i < buf1.shape[0]; i++)
    {
        ptr3[i] = ptr1[i] + ptr2[i];
    }

    return result;

}

/*
2d矩阵相加
*/
py::array_t<double> add_arrays_2d(py::array_t<double>& input1, py::array_t<double>& input2) {

    py::buffer_info buf1 = input1.request();
    py::buffer_info buf2 = input2.request();

    if (buf1.ndim != 2 || buf2.ndim != 2)
    {
        throw std::runtime_error("numpy.ndarray dims must be 2!");
    }
    if ((buf1.shape[0] != buf2.shape[0])|| (buf1.shape[1] != buf2.shape[1]))
    {
        throw std::runtime_error("two array shape must be match!");
    }

    //申请内存
    auto result = py::array_t<double>(buf1.size);
    //转换为2d矩阵
    result.resize({buf1.shape[0],buf1.shape[1]});


    py::buffer_info buf_result = result.request();

    //指针访问读写 numpy.ndarray
    double* ptr1 = (double*)buf1.ptr;
    double* ptr2 = (double*)buf2.ptr;
    double* ptr_result = (double*)buf_result.ptr;

    for (int i = 0; i < buf1.shape[0]; i++)
    {
        for (int j = 0; j < buf1.shape[1]; j++)
        {
            auto value1 = ptr1[i*buf1.shape[1] + j];
            auto value2 = ptr2[i*buf2.shape[1] + j];

            ptr_result[i*buf_result.shape[1] + j] = value1 + value2;
        }
    }

    return result;

}

/*
numpy.ndarray 相加，  3d矩阵
@return 3d numpy.ndarray
*/
py::array_t<double> add_arrays_3d(py::array_t<double>& input1, py::array_t<double>& input2) {

    //unchecked<N> --------------can be non-writeable
    //mutable_unchecked<N>-------can be writeable
    auto r1 = input1.unchecked<3>();
    auto r2 = input2.unchecked<3>();

    py::array_t<double> out = py::array_t<double>(input1.size());
    out.resize({ input1.shape()[0], input1.shape()[1], input1.shape()[2] });
    auto r3 = out.mutable_unchecked<3>();

    for (int i = 0; i < input1.shape()[0]; i++)
    {
        for (int j = 0; j < input1.shape()[1]; j++)
        {
            for (int k = 0; k < input1.shape()[2]; k++)
            {
                double value1 = r1(i, j, k);
                double value2 = r2(i, j, k);

                //下标索引访问 numpy.ndarray
                r3(i, j, k) = value1 + value2;
            
            }
        }
    }

    return out;

}

PYBIND11_MODULE(numpy_demo2, m) {

    m.doc() = "Simple demo using numpy!";

    m.def("add_arrays_1d", &add_arrays_1d);
    m.def("add_arrays_2d", &add_arrays_2d);
    m.def("add_arrays_3d", &add_arrays_3d);
}

