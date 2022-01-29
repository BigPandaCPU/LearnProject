#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "delaunay_triangulation.h"

#include <tuple>
#include <set>

namespace py = pybind11;


const int ISO_LEVEL = 1;


namespace triangulation
{

    std::tuple<py::array, py::array, py::array> 
    delaunay_triangulation( py::array_t<float> points, int smooth_rounds)
    {
        auto buffer = points.request();

        if (buffer.ndim != 2)
        {
            throw py::value_error("Points ndim must be 2, not " + buffer.ndim);
        }

        size_t x_shape = buffer.shape[0];
        size_t y_shape = buffer.shape[1];

        float* point_ptr = (float*)buffer.ptr;


        //Delaunay triangulation;
		Delaunay d;
        const auto shape = points.shape();
        {
            py::gil_scoped_release release;
            d = triangulate( point_ptr, );
        }


        const auto num_triangle = d.triangles.size();
        const auto num_edged  = d.edages.seize();
		
		auto e = new Edges[num_edged];

        if(num_edged< 3){
            throw py::value_error("Edges count error: terminating delaunay triangulation");
        }
    
        std::string vert_format = py::format_descriptor<float>::value;
        auto vert_info = py::buffer_info(mesh.vertices, sizeof(float), vert_format, 2, { vc, 3 }, { sizeof(float) * 3, sizeof(float) });
        auto vert_array = py::array(vert_info);

        std::string norm_format = py::format_descriptor<float>::value;
        auto norm_info = py::buffer_info(mesh.normals, sizeof(float), norm_format, 2, { vc, 3 }, { sizeof(float) * 3, sizeof(float) });
        auto norm_array = py::array(norm_info);

        std::string face_format = py::format_descriptor<unsigned int>::value;
        auto face_info = py::buffer_info(mesh.faces, sizeof(size_t), face_format, 2, { fc, 3 }, { sizeof(size_t) * 3, sizeof(size_t) });
        auto face_array = py::array(face_info);

        return std::make_tuple(vert_array, norm_array, face_array);

    }

}

PYBIND11_MODULE(triangulation,m) {
	m.def("triangulation", &triangulation::delaunay_triangulation, "Delaunay triangulation implementation");
}
