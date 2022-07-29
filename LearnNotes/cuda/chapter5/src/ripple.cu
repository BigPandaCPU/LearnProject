/* Copyright (c) 1993-2015, NVIDIA CORPORATION. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *  * Neither the name of NVIDIA CORPORATION nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 * OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
#include <stdlib.h>
#include <stdio.h>
#include"../common/book.h"
#include"../common/image.h"

#define DIM 1024
#define PI 3.1415926535f

__global__ void kernel(unsigned char *ptr, int ticks)
{
	__shared__ float shared[16][16];

	int x = threadIdx.x + blockIdx.x*blockDim.x;
	int y = threadIdx.y + blockIdx.y*blockDim.y;
	int offset = x + y * blockDim.x*gridDim.x;
	const float period = 128.0f;

	float fx = x - DIM / 2;
	float fy = y - DIM / 2;
	float d = sqrtf(fx*fx + fy * fy);
	//unsigned char grey = (unsigned char)(128.0f + 127.0f*
	//									cos(d / 10.0f - ticks / 7.0f) / 
	//									(d / 10.0f + 1.0f));
	shared[threadIdx.x][threadIdx.y] = 255 * (sinf(x*2.0f*PI / period) + 1.0f)*
		(sinf(y*2.0f*PI / period) + 1.0f) / 4.0f;
	__syncthreads();

	ptr[offset * 4 + 0] = 0;
	ptr[offset * 4 + 1] = shared[threadIdx.x][threadIdx.y];
	ptr[offset * 4 + 2] = 0;
	ptr[offset * 4 + 3] = 255;
}

struct DataBlock
{
	unsigned char *dev_bitmap;
	IMAGE *bitmap;
};

void cleanup(DataBlock* d)
{
	HANDLE_ERROR(cudaFree(d->dev_bitmap));
}

int main(void)
{
	DataBlock data;
	IMAGE bitmap(DIM, DIM);
	data.bitmap = &bitmap;
	HANDLE_ERROR(cudaMalloc((void**)&data.dev_bitmap, bitmap.image_size()));

	dim3 blocks(DIM / 16, DIM / 16);
	dim3 threads(16, 16);

	int ticks = 0;
	bitmap.show_image(30);
	//while (1)
	//{
	kernel <<<blocks, threads >>> (data.dev_bitmap, ticks);
	HANDLE_ERROR(cudaMemcpy(data.bitmap->get_ptr(), data.dev_bitmap, data.bitmap->image_size(), cudaMemcpyDeviceToHost));

	ticks++;
	bitmap.show_image();
	//if (key == 27)
	//{
	//	break;
	//}
	//}
	cleanup(&data);
	return 0;
}



