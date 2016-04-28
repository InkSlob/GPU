#include <stdio.h>
#include <stdlib.h>
#include <cuda.h>

 #define N 5

 __global__ void Add(int *a, int*b, int *c){
 int i = blockIdx.x; 
 if(i<N){
 c[i] = a[i] + b[i];   
 }
}

 int main(){
 int a[N] = {1,2,3,4,5}, b[N] = {5,6,7,8,9}; 
 int c[N];
 int *dev_a, *dev_b, *dev_c; 


 cudaMalloc((void**)&dev_a, N*sizeof(int));
 cudaMalloc((void**)&dev_b, N*sizeof(int));
 cudaMalloc((void**)&dev_c, N*sizeof(int));


 cudaMemcpy(dev_a, a, N*sizeof(int), cudaMemcpyHostToDevice); 
 cudaMemcpy(dev_b, b, N*sizeof(int), cudaMemcpyHostToDevice);

 Add<<<2,1>>>(dev_a, dev_b, dev_c); // HERE IS THE CRITICAL LINE !!!!!!


 cudaMemcpy(c, dev_c, N*sizeof(int), cudaMemcpyDeviceToHost);


 int i; printf("c[i] = ");
 for(i=0;i<N;i++){
    printf("%d ", c[i]);
 }


 cudaFree(dev_a); 
 cudaFree(dev_b); 
 cudaFree(dev_c);

 printf("\n");
 return 0;
 }