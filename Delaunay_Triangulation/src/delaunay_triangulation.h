/*
* Bowyer-Watson algorithm
* C++ implementation of http://paulbourke.net/paper/trianglulate
*/

#pragma once

#include <algorithm>
#include <iostream>
#include <vector>

namespace delaunay 
{
    constexpr double eps = 1e-4;
    typedef float PointOut[2];
    struct Point 
	{
        float x, y;

        Point() : x{ 0.0 }, y{ 0.0 } {}
        Point(float _x, float _y) : x{ _x }, y{ _y } {}
        Point(const Point& p):x(p.x),y(p.y){}


        friend std::ostream& operator<<(std::ostream& os, const Point& p)
        {
            os << "x=" << p.x << "  y=" << p.y;
            return os;
        }

        bool operator==(const Point& other) const
        {
            return (other.x == x && other.y == y);
        }

        bool operator!=(const Point& other) const { return !operator==(other); }
    };
    struct Edge 
	{
        using Node = Point;
        Node p0, p1;
		Edge():p0(Point(0,0)),p1(Point(0,0)){}

        Edge(Node const& _p0, Node const& _p1) : p0{ _p0 }, p1{ _p1 } {}

        friend std::ostream& operator<<(std::ostream& os, const Edge& e)
        {
            os << "p0: [" << e.p0 << " ] p1: [" << e.p1 << "]";
            return os;
        }

        bool operator==(const Edge& other) const
        {
            return ((other.p0 == p0 && other.p1 == p1) ||
                (other.p0 == p1 && other.p1 == p0));
        }
    };

    struct Circle 
	{
        float x, y, radius;
        Circle() = default;
    };

    struct Triangle 
	{
        using Node = Point;
        Node p0, p1, p2;
        Edge e0, e1, e2;
        Circle circle;

        Triangle(const Node& _p0, const Node& _p1, const Node& _p2)
            : p0{ _p0 },
            p1{ _p1 },
            p2{ _p2 },
            e0{ _p0, _p1 },
            e1{ _p1, _p2 },
            e2{ _p0, _p2 },
            circle{}
        {
            const auto ax = p1.x - p0.x;
            const auto ay = p1.y - p0.y;
            const auto bx = p2.x - p0.x;
            const auto by = p2.y - p0.y;

            const auto m = p1.x * p1.x - p0.x * p0.x + p1.y * p1.y - p0.y * p0.y;
            const auto u = p2.x * p2.x - p0.x * p0.x + p2.y * p2.y - p0.y * p0.y;
            const auto s = 1. / (2.0 * (ax * by - ay * bx));

            circle.x = ((p2.y - p0.y) * m + (p0.y - p1.y) * u) * s;
            circle.y = ((p0.x - p2.x) * m + (p1.x - p0.x) * u) * s;

            const auto dx = p0.x - circle.x;
            const auto dy = p0.y - circle.y;
            circle.radius = dx * dx + dy * dy;
        }
    };
    struct TriangleOut
    {
        Point p0, p1, p2;
        TriangleOut(const Point& _p0, const Point& _p1, const Point& _p2):p0(_p0),p1(_p1),p2(_p2){}
        TriangleOut(const TriangleOut& tri):p0(tri.p0),p1(tri.p1),p2(tri.p2){}
    };

    struct Delaunay
    {
        std::vector<Triangle> triangles;
        std::vector<Edge> edges;
    };

    Delaunay triangulate(const Point* points, int num_point, int dim=2);
}
    
