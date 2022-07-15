#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "delaunay_triangulation.h"

#include <tuple>
#include <set>

namespace py = pybind11;


const int ISO_LEVEL = 1;


namespace triangulation
{

  py::array_t<float> delaunay_triangulation( py::array_t<float> points, int smooth_rounds)
    {
        auto buffer = points.request();

        if (buffer.ndim != 2)
        {
            throw py::value_error("Points ndim must be 2, not " + buffer.ndim);
        }

        size_t num_points = buffer.shape[0];
        size_t num_dims = buffer.shape[1];

        const float* data_ptr = (float*)buffer.ptr;
        delaunay::Point* point_ptr = new delaunay::Point[num_points];
        for(size_t i=0; i< num_points; i++)
        {
            float x = data_ptr[i*2];
            float y = data_ptr[i*2+1];
            point_ptr[i] = delaunay::Point(x,y);
        }
        //Delaunay triangulation;
		delaunay::Delaunay d;
        const auto shape = points.shape();
        {
            py::gil_scoped_release release;
            d = delaunay::triangulate( point_ptr, num_points );
        }


        const auto num_triangle = d.triangles.size();
        const auto num_edged  = d.edges.size();
		

		//auto tri = new delaunay::PointOut[num_triangle*3];
		auto tri_out = py::array_t<float>(num_triangle*3*2);
		py::buffer_info buf = tri_out.request();
		float* tri = (float*)buf.ptr;
		/*auto e = new Edges[num_edged];
		for(int i=0; i<num_edged; i++)
		{
		    e[i] = d.edage[i];
		}*/

		for(size_t i=0; i< num_triangle; i++)
		{
		    tri[i*6+0] = d.triangles[i].p0.x;
		    tri[i*6+1] = d.triangles[i].p0.y;

		    tri[i*6+2] = d.triangles[i].p1.x;
		    tri[i*6+3] = d.triangles[i].p1.y;

		    tri[i*6+4] = d.triangles[i].p2.x;
		    tri[i*6+5] = d.triangles[i].p2.y;
		}

        /*if(num_edged< 3){
            throw py::value_error("Edges count error: terminating delaunay triangulation");
        }*/


        //std::string tri_format = py::format_descriptor<float>::value;
        //auto tri_info = py::buffer_info(tri, sizeof(float), tri_format, 2, { num_triangle*3, 2}, { sizeof(float) * 2, sizeof(float) });
        //auto tri_array = py::array(tri_info);
        //return std::make_tuple(tri_array);
        return tri_out;
    }

}

PYBIND11_MODULE(DelaunayTriangulation,m) {
	m.def("triangulation", &triangulation::delaunay_triangulation, "Delaunay triangulation implementation");
}
