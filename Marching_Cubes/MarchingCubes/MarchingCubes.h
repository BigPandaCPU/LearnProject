#pragma once
#include<iostream>

typedef struct
{
	float x, y, z;
} XYZ;
typedef struct
{
	XYZ p[8];
	XYZ n[8];
	float val[8];
}GRIDCELL;

typedef struct
{
	XYZ p[3];     /*Vertices*/
	XYZ c;        /*Centroid*/
	XYZ n[3];     /*Normal*/

}TRIANGLE;

#define ABS(x) ( x < 0 ? -(x) : (x) )

int PolygoniseCube(GRIDCELL, double, TRIANGLE*);
XYZ VertexInterp(double, XYZ, XYZ, double, double);

bool ExportFileSTLBinary(std::string filePath, const std::string & headerInfo, const TRIANGLE *tri, const int& triangleCount);