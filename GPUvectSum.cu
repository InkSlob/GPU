#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gsl/gsl_cblas.h>
#include <cuda.h>

#define N   10


__global__ void Add(int *a, int*b, int *c){
 int i = blockIdx.x; 
 if(i<N){
 c[i] = a[i] + b[i];   
 }
}





int main(void) {
	int a[N], b[N], c[N];
	int *dev_a, *dev_b, *dev_c;
	
	//allocate the memory on the GPU
	cudaMalloc((void**)&dev_a, N * sizeof(int));
	cudaMalloc((void**)&dev_b, N * sizeof(int));
	cudaMalloc((void**)&dev_c, N * sizeof(int));
	
	//fill the array's 'a' and 'b' on the CPU
	for (int i=0; i<N; i++){
		a[i] = -i;
		b[i] = i * i;
	}
	
	//copy the arrays 'a' and 'b' to the GPU
	cudaMemcpy(dev_a, a, N * sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(dev_b, b, N * sizeof(int), cudaMemcpyHostToDevice);
	cudaMemcpy(dev_c, c, N*sizeof(int), cudaMemcpyHostToDevice);
	
	double rMean[8] = {3.15,1.75,-6.4,-2.9,-6.8,-0.54,-6.8,-5.3};
	double covMatrix[8][8] = {
	  {0.001005, 0.001328, -0.000579, -0.000675, 0.000121, 0.000128, -0.000445, -0.000437},
	  {0.001328, 0.007277, -0.001307, -0.00061, -0.002237, -0.000989, 0.001442, -0.001535},	
	  {-0.000579, -0.001307, 0.059852, 0.027588, 0.063497, 0.023036, 0.032967, 0.048039},
	  {-0.000675, -0.00061, 0.027588, 0.029609, 0.026572, 0.021465, 0.020697, 0.029854}, 
	  {0.000121, -0.002237, 0.063497, 0.026572, 0.102488, 0.042744, 0.039943, 0.065994}, 
	  {0.000128, -0.000989, 0.023036, 0.021465, 0.042744, 0.032056, 0.019881, 0.032235}, 
	  {-0.000445, 0.001442, 0.032967, 0.020697, 0.039943, 0.019881, 0.028355, 0.035064},
	  {-0.000437, -0.001535, 0.048039, 0.029854, 0.065994, 0.032235, 0.035064, 0.079958}
	};
	
	
	
	Add<<<N,1>>>( dev_a, dev_b, dev_c);
	
	
	//copy the array 'c' back from the GPU to the CPU
	cudaMemcpy(c, dev_c, N*sizeof(int), cudaMemcpyDeviceToHost);
	
	// display the results
	int i; 
	for(i=0; i<N; i++){
		printf("%d", a[i], "%d",  b[i], "%d",  c[i], "\r\n");
	}
	
	// free the memory allocated on the GPU
	cudaFree( dev_a);
	cudaFree( dev_b);
	cudaFree( dev_c);
	
	return 0;
}