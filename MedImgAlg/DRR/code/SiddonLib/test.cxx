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

#define EPS 1e-6 

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

int main( void ) 
{

	constexpr unsigned int Dimension = 3;
	char file_names[100]="data/spine1.nii.gz";
	using PixelType = float;
	using ImageType = itk::Image<PixelType, Dimension>;

	ImageType::Pointer image = itk::ReadImage<ImageType>(file_names);
	image->Update();
	printf("spacing[0] = %f\n",image->GetSpacing()[0]);
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
	DRRSize[0] = 1300;
	DRRSize[1] = 1500;
	DRRSize[2] = 1;

	float *DRRSpacing = new float[Dimension];
	DRRSpacing[0] = 0.25;
	DRRSpacing[1] = 1.0;
	DRRSpacing[2] = 0.25;


	SiddonGpu* siddonGpu = new SiddonGpu(numThreadsPerBlock, movImgArray, movSize, movSpacing, X0, Y0, Z0, DRRSize);


	

	const float VCS = 950.0; //volume center to source point
	const float VCD = 350.0; //volume center to detector
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

	clock_t time_start, time_end;
	float total_time;
	time_start = clock();
	siddonGpu->generateDRR(source_point, DestArray, drrArray);
	time_end = clock();
	total_time = (float)(time_end - time_start) / CLOCKS_PER_SEC;
	std::cout << "DRR time:" << total_time << std::endl;
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


