/*
* Bowyer-Watson algorithm
* C++ implementation of http://paulbourke.net/paper/trianglulate
*/

#pragma once

#include <algorithm>
#include <iostream>
#include <vector>
#include "delauay_triangulation.h"

namespace delaunay 
{
    Delaunay triangulate(const Point* p, int num_point, int dim)
    {
		std::vector<Point> points;
		for(int i=0; i <num_point; i++)
		{
			points.push_back(p[i]);
		}
		
        using Node = Point;

        if( points.size()<3 )
        {
            return Delaunay{};
        }
        auto xmin = points[0].x;
        auto xmax = xmin;
        auto ymin = points[0].y;
        auto ymax = ymin;
        for (auto const& pt : points)
        {
            xmin = std::min(xmin, pt.x);
            xmax = std::max(xmax, pt.x);
            ymin = std::min(ymin, pt.y);
            ymax = std::max(ymax, pt.y);
        }

        const auto dx = xmax - xmin;
        const auto dy = ymax - ymin;
        const auto dmax = std::max(dx, dy);
        const auto midx = (xmin + xmax) / 2.0;
        const auto midy = (ymin + ymax) / 2.0;


        auto d = Delaunay{};
        const auto p0 = Node{ midx - 20 * dmax, midy - dmax };
        const auto p1 = Node{ midx, midy + 20 * dmax };
        const auto p2 = Node{ midx + 20 * dmax, midy - dmax };

        d.triangles.emplace_back(Triangle{p0, p1, p2});

        for (auto const& pt : points)
        {
            std::vector<Edge> edges;
            std::vector<Triangle> tmps;
            for (auto const& tri : d.triangles) 
            {
                /* check if the point is inside the triangle circlumcircle. */
                const auto dist = (tri.circle.x - pt.x) * (tri.circle.x - pt.x) +
                    (tri.circle.y - pt.y) * (tri.circle.y - pt.y);
                if ((dist - tri.circle.radius) <= eps)
                {
                    edges.push_back(tri.e0);
                    edges.push_back(tri.e1);
                    edges.push_back(tri.e2);
                }
                else
                {
                    tmps.push_back(tri);
                }
            }
			
			/* Delete duplicate edges. */
			std::vector<bool> remove(edges.size(), false);
			for (auto it1 = edges.begin(); it1 != edges.end(); ++it1) 
			{
			  for (auto it2 = edges.begin(); it2 != edges.end(); ++it2) {
				if (it1 == it2) {
				  continue;
				}
				if (*it1 == *it2) {
				  remove[std::distance(edges.begin(), it1)] = true;
				  remove[std::distance(edges.begin(), it2)] = true;
				}
			  }
			}

			edges.erase(
				std::remove_if(edges.begin(), edges.end(),
							   [&](auto const& e) { return remove[&e - &edges[0]]; }),
				edges.end());

			/* Update triangulation. */
			for (auto const& e : edges) 
			{
			  tmps.push_back({e.p0, e.p1, {pt.x, pt.y}});
			}
			d.triangles = tmps;
		}

		/* Remove original super triangle. */
		d.triangles.erase(
			std::remove_if(d.triangles.begin(), d.triangles.end(),
							 [&](auto const& tri) {
							   return ((tri.p0 == p0 || tri.p1 == p0 || tri.p2 == p0) ||
									   (tri.p0 == p1 || tri.p1 == p1 || tri.p2 == p1) ||
									   (tri.p0 == p2 || tri.p1 == p2 || tri.p2 == p2));
							 }),
			d.triangles.end());

		/* Add edges. */
		for (auto const& tri : d.triangles) 
		{
			d.edges.push_back(tri.e0);
			d.edges.push_back(tri.e1);
			d.edges.push_back(tri.e2);
		}
		return d
	}
}