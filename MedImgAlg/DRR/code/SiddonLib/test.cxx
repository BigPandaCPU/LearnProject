/*
 * Copyright 1993-2010 NVIDIA Corporation.  All rights reserved.
 *
 * NVIDIA Corporation and its licensors retain all intellectual property and 
 * proprietary rights in and to this software and related documentation. 
 * Any use, reproduction, disclosure, or distribution of this software 
 * and related documentation without an express license agreement from
 * NVIDIA Corporation is strictly prohibited.
 *
 * Please refer to the applicable NVIDIA end user license agreement (EULA) 
 * associated with this source code for terms and conditions that govern 
 * your use of this NVIDIA software.
 * 
 */


//#include "book.h"

#include "itkImage.h"
#include "itkImageFileReader.h"
#include "siddon_class.cuh"
#include <itkPhysicalPointImageSource.h>
#include "itkVector.h"
#include "itkPointSet.h"
#include<time.h>
#include<math.h>

#define EPS 1e-6 

#define PI acos(-1)

void HU2Myu(float* imageArray, int imageSize,float myu_water=0.2683)
{
	for (auto i = 0; i < imageSize; i++)
	{
		if (imageArray[i] < EPS)
		{
			imageArray[i] = 0.0;
		}
		else
		{
			imageArray[i] = imageArray[i] / 1000.0*myu_water;
		}
	}
}

void getRigidMotionMatFromEuler(float **rotTransMatrix, float rotx = 0.0f, float roty = 0.0f, float rotz = 0.0f, float transx = 0.0f, float transy = 0.0f, float transz = 0.0f)
{
	float rotXMatrix[3][3] = { 0.0f };
	float rotYMatrix[3][3] = { 0.0f };
	float rotZMatrix[3][3] = { 0.0f };

	rotXMatrix[0][0] = 1.0f;
	rotXMatrix[1][1] = cos(rotx);
	rotXMatrix[1][2] = -sin(rotx);
	rotXMatrix[2][1] = sin(rotx);
	rotXMatrix[2][2] = cos(rotx);

	rotYMatrix[0][0] = cos(roty);
	rotYMatrix[0][2] = sin(roty);
	rotYMatrix[1][1] = 1.0f;
	rotYMatrix[2][0] = -sin(roty);
	rotYMatrix[2][2] = cos(roty);

	rotZMatrix[0][0] = cos(rotz);
	rotZMatrix[0][1] = -sin(rotz);
	rotZMatrix[1][0] = sin(rotz);
	rotZMatrix[1][1] = cos(rotz);
	rotZMatrix[2][2] = 1.0f;

	float tmp[3][3] = { 0.0f };

	for (int i = 0; i < 3; i++)
	{
		for (int j = 0; j < 3; j++)
			tmp[i][j] = rotXMatrix[i][0] * rotYMatrix[0][j] +
						rotXMatrix[i][1] * rotYMatrix[1][j] +
						rotXMatrix[i][2] * rotYMatrix[2][j];
	}

	for (int i = 0; i < 3; i++)
	{
		for (int j = 0; j < 3; j++)
			rotTransMatrix[i][j] = tmp[i][0] * rotZMatrix[0][j] +
								   tmp[i][1] * rotZMatrix[1][j] +
								   tmp[i][2] * rotZMatrix[2][j];

	}

	rotTransMatrix[0][3] = transx;
	rotTransMatrix[1][3] = transy;
	rotTransMatrix[2][3] = transz;
}


int main(void)
{
	constexpr unsigned int Dimension = 3;
	char file_names[100] = "data/spine1.nii.gz";
	using PixelType = float;
	using ImageType = itk::Image<PixelType, Dimension>;

	ImageType::Pointer image = itk::ReadImage<ImageType>(file_names);
	image->Update();
	printf("spacing[0] = %f\n", image->GetSpacing()[0]);
	printf("spacing[1] = %f\n", image->GetSpacing()[1]);
	printf("spacing[2] = %f\n", image->GetSpacing()[2]);

	printf("origin[0] = %f\n", image->GetOrigin()[0]);
	printf("origin[1] = %f\n", image->GetOrigin()[1]);
	printf("origin[2] = %f\n", image->GetOrigin()[2]);

	printf("size[0] = %d\n", image->GetBufferedRegion().GetSize()[0]);
	printf("size[1] = %d\n", image->GetBufferedRegion().GetSize()[1]);
	printf("size[2] = %d\n", image->GetBufferedRegion().GetSize()[2]);

	//int aim_idx = (949 - 1) * 512 * 512 + (310 - 1) * 512 + (325-1);
	//float * p = image->GetBufferPointer();
	//printf("aim value[%d]:%f\n",aim_idx, p[aim_idx]);
	//printf("aim value[%d]:%f\n", aim_idx + 10, p[aim_idx + 10]);
	//for (auto i = 0; i < 10; i++)
	//{
	//	printf("%d, %f\n",i, p[i]);
	//}


	int *numThreadsPerBlock;
	float *movImgArray;
	int *movSize;
	float *movSpacing;
	float X0;
	float Y0;
	float Z0;
	int *DRRSize;

	numThreadsPerBlock = new int[3];
	numThreadsPerBlock[0] = 16;
	numThreadsPerBlock[1] = 16;
	numThreadsPerBlock[2] = 1;

	int xdim = image->GetBufferedRegion().GetSize()[0];
	int ydim = image->GetBufferedRegion().GetSize()[1];
	int zdim = image->GetBufferedRegion().GetSize()[2];
	movImgArray = image->GetBufferPointer();

	//Convert CT images represented in Hu to linear attenuation coefficient
	HU2Myu(movImgArray, xdim*ydim*zdim);

	movSize = new int[Dimension];
	movSize[0] = xdim;
	movSize[1] = ydim;
	movSize[2] = zdim;

	float xSpacing = image->GetSpacing()[0];
	float ySpacing = image->GetSpacing()[1];
	float zSpacing = image->GetSpacing()[2];

	movSpacing = new float[Dimension];
	movSpacing[0] = xSpacing;
	movSpacing[1] = ySpacing;
	movSpacing[2] = zSpacing;

	X0 = image->GetOrigin()[0];
	Y0 = image->GetOrigin()[1];
	Z0 = image->GetOrigin()[2];

	DRRSize = new int[Dimension];
	DRRSize[0] = 1500;
	DRRSize[1] = 1500;
	DRRSize[2] = 1;

	float *DRRSpacing = new float[Dimension];
	DRRSpacing[0] = 0.3;
	DRRSpacing[1] = 1.0;
	DRRSpacing[2] = 0.3;


	SiddonGpu* siddonGpu = new SiddonGpu(numThreadsPerBlock, movImgArray, movSize, movSpacing, X0, Y0, Z0, DRRSize);


	const float VCS = 950.0;
	const float VCD = 300.0;
	float volume_center_x = X0 + movSize[0] / 2.0*movSpacing[0];
	float volume_center_y = Y0 + movSize[1] / 2.0*movSpacing[1];
	float volume_center_z = Z0 + movSize[2] / 2.0*movSpacing[2];


	float *source_point = new float[Dimension];
	source_point[0] = volume_center_x;
	source_point[1] = volume_center_y - VCS;
	source_point[2] = volume_center_z;

	float *drrArray = new float[DRRSize[0] * DRRSize[1] * DRRSize[2]];
	float *DestArray;

	ImageType::Pointer drrImage = ImageType::New();
	ImageType::IndexType start;

	start[0] = 0; // first index on X
	start[1] = 0; // first index on Y
	start[2] = 0; // first index on Z

	ImageType::SizeType size;

	size[0] = DRRSize[0]; // size along X
	size[1] = 1; // size along Y
	size[2] = DRRSize[1]; // size along Z

	float drrOrigin_x = volume_center_x - DRRSpacing[0] * (size[0] - 1.0) / 2.0;
	float drrOrigin_y = volume_center_y + VCD;
	float drrOrigin_z = volume_center_z - DRRSpacing[2] * (size[2] - 1.0) / 2.0;

	const itk::SpacePrecisionType drrOigin[Dimension] = { drrOrigin_x, drrOrigin_y, drrOrigin_z };
	const itk::SpacePrecisionType drrSpacing[Dimension] = { DRRSpacing[0], DRRSpacing[1], DRRSpacing[2] };

	ImageType::RegionType region;

	region.SetSize(size);
	region.SetIndex(start);

	drrImage->SetRegions(region);
	drrImage->Allocate();
	drrImage->SetDirection(image->GetDirection());
	drrImage->SetSpacing(drrSpacing);
	drrImage->SetOrigin(drrOigin);

	std::cout << "\nstep2:" << std::endl;

	using VectorPixelType = itk::Vector<float, Dimension>;
	using PhyImageType = itk::Image<VectorPixelType, Dimension>;

	using PhysicalPointImagefilterType = itk::PhysicalPointImageSource<PhyImageType>;
	PhysicalPointImagefilterType::Pointer physicalPointerImagefilter = PhysicalPointImagefilterType::New();
	physicalPointerImagefilter->SetReferenceImage(drrImage);
	physicalPointerImagefilter->SetUseReferenceImage(true);
	physicalPointerImagefilter->Update();

	std::cout << "\nstep3:" << std::endl;
	PhyImageType::Pointer output = physicalPointerImagefilter->GetOutput();
	VectorPixelType *yy = output->GetBufferPointer();
	DestArray = yy->data();
	std::cout << yy[0] << std::endl;
	std::cout << yy[1] << std::endl;
	std::cout << yy[2] << std::endl;
	std::cout << yy[3] << std::endl;

	std::cout << "\nstep4:" << std::endl;

	for (int i = 0; i < 15; i++)
	{
		std::cout << "DestArray[" << i << "]=" << DestArray[i] << std::endl;
	}

	clock_t time_start, time_end;
	float total_time;
	time_start = clock();


	float **rotTransMatrix = new float*[3];
	for (int i = 0; i < 4; i++)
	{
		rotTransMatrix[i] = new float[4];
	}
	float volumeCenterTransMatrix[3][4] = { 0.0f };
	float invVolumeCenterTransMatrix[3][4] = { 0.0f };

	volumeCenterTransMatrix[0][0] = 1.0f;
	volumeCenterTransMatrix[1][1] = 1.0f;
	volumeCenterTransMatrix[2][2] = 1.0f;
	volumeCenterTransMatrix[0][3] = -volume_center_x;
	volumeCenterTransMatrix[1][3] = -volume_center_y;
	volumeCenterTransMatrix[2][3] = -volume_center_z;

	invVolumeCenterTransMatrix[0][0] = 1.0f;
	invVolumeCenterTransMatrix[1][1] = 1.0f;
	invVolumeCenterTransMatrix[2][2] = 1.0f;

	invVolumeCenterTransMatrix[0][3] = volume_center_x;
	invVolumeCenterTransMatrix[1][3] = volume_center_y;
	invVolumeCenterTransMatrix[2][3] = volume_center_z;

	float tmp[3][4] = { 0.0f };
	float finalRotTransMatrix[3][4] = { 0.0f };

	float *new_source_point = new float[Dimension];
	float *new_DestArray = new float[DRRSize[0] * DRRSize[1] * Dimension];

	const int N = 12;

	for (int rotYI = -N; rotYI < N + 1; rotYI++)
	{
		//for (int j = -N; j < N + 1; j++)

		{
			float roty = (-8*5.0) / 180.0*PI;
			//float rotx = (j*5.0) / 180.0*PI;

			getRigidMotionMatFromEuler(rotTransMatrix, 0.0, roty, 0.0, 0.0, 0.0, 0.0);

			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++)
				{
					tmp[i][j] = invVolumeCenterTransMatrix[i][0] * rotTransMatrix[0][j] +
						invVolumeCenterTransMatrix[i][1] * rotTransMatrix[1][j] +
						invVolumeCenterTransMatrix[i][2] * rotTransMatrix[2][j];
				}

				tmp[i][3] = invVolumeCenterTransMatrix[i][0] * rotTransMatrix[0][3] +
					invVolumeCenterTransMatrix[i][1] * rotTransMatrix[1][3] +
					invVolumeCenterTransMatrix[i][2] * rotTransMatrix[2][3] +
					invVolumeCenterTransMatrix[i][3] * 1.0f;
			}

			for (int i = 0; i < 3; i++)
			{
				for (int j = 0; j < 3; j++)
				{

					finalRotTransMatrix[i][j] = tmp[i][0] * volumeCenterTransMatrix[0][j] +
						tmp[i][1] * volumeCenterTransMatrix[1][j] +
						tmp[i][2] * volumeCenterTransMatrix[2][j];
				}
				finalRotTransMatrix[i][3] = tmp[i][0] * volumeCenterTransMatrix[0][3] +
					tmp[i][1] * volumeCenterTransMatrix[1][3] +
					tmp[i][2] * volumeCenterTransMatrix[2][3] +
					tmp[i][3] * 1.0f;
			}


			for (int i = 0; i < Dimension; i++)
			{
				new_source_point[i] = finalRotTransMatrix[i][0] * source_point[0] +
					finalRotTransMatrix[i][1] * source_point[1] +
					finalRotTransMatrix[i][2] * source_point[2] +
					finalRotTransMatrix[i][3] * 1.0f;
			}

			for (int i = 0; i < DRRSize[0] * DRRSize[1]; i++)
			{
				for (int j = 0; j < Dimension; j++)
				{
					new_DestArray[i*Dimension + j] = finalRotTransMatrix[j][0] * DestArray[i*Dimension + 0] +
						finalRotTransMatrix[j][1] * DestArray[i*Dimension + 1] +
						finalRotTransMatrix[j][2] * DestArray[i*Dimension + 2] +
						finalRotTransMatrix[j][3] * 1.0f;
				}
			}

			siddonGpu->generateDRR(new_source_point, new_DestArray, drrArray);

			char saveFileName[100];
			sprintf(saveFileName, "drr_rotY_%d.txt", rotYI*5);
			std::cout << saveFileName << std::endl;

			FILE *fp = fopen(saveFileName, "w");
			for (int j = 0; j < DRRSize[1]; j++)
			{
				for (int i = 0; i < DRRSize[0]; i++)
				{
					fprintf(fp, "%f  ", drrArray[j*DRRSize[0] + i]);
				}
				fprintf(fp, "\n");
			}
			fclose(fp);


		}
	}
		

	time_end = clock();
	total_time = (float)(time_end - time_start) / CLOCKS_PER_SEC;
	std::cout << "DRR times:" <<4*N*N<<", total times:"<<total_time << std::endl;
	std::cout << "\nstep5:" << std::endl;
	

	std::cout << "\nDRR image:" << std::endl;
	std::cout << drrArray[0] << std::endl;
	std::cout << drrArray[1] << std::endl;
	std::cout << drrArray[2] << std::endl;


	FILE *fp = fopen("drr.txt", "w");
	for (int j = 0; j < DRRSize[1]; j++)
	{
		for (int i = 0; i < DRRSize[0]; i++)
		{
			fprintf(fp, "%f  ", drrArray[j*DRRSize[0] + i]);
		}
		fprintf(fp, "\n");
	}
	fclose(fp);
	
	printf("Siddon constructor down!\n");

    return 0;
}


