from numbapro import guvectorize
from numpy import arange
#!/usr/bin/python
from scipy import linalg
from scipy.linalg import *
import numpy as np
from numbapro import guvectorize
from numba import *
from numbapro import cuda
import math
from numpy import arange
import sys
import csv

def fileCov(na):
	rmean = zeros(na)
	y = zeros((na, na))
    # 8 x 8 array
	with open('covMatrix.csv', 'r') as f1:
		reader = csv.reader(f1)
		i = 0
    
		for row in reader:
			y[i] = np.array(row, float64)
			i = i +1
			
    # 8 x 1 array                    
	with open('rMean.csv', 'r') as f2:
		reader = csv.reader(f2)
		for row in reader:
			rmean = np.array(row, float64)
	return rmean, y

@guvectorize(['void(float64[:,:], float64[:,:], float64[:,:])'],
             '(m,n),(n,p)->(m,p)')
def matmul(A, B, C):
    m, n = A.shape
    n, p = B.shape
    for i in range(m):
        for j in range(p):
            C[i, j] = 0
            for k in range(n):
                C[i, 0] += A[i, k] * B[k,0]

@cuda.jit(argtypes=(double[:,:], double[:,:]), restype=double, device=True, inline=True)
def gpuSolver(x, B):
    linalg.inv(x).dot(B)

w = 2
na = 8
rmean, y = fileCov(na)
x = zeros((1,na))
xs = zeros((1,na))
A = y
B = rmean
C = matmul(A, B)
xs = gpuSolver
print xs
print("A:\n%s" % A)
print("B:\n%s" % B)
print("C:\n%s" % C)
LR = gpusolve(A, C)
print LR
sum = 0.0
for j in range(na):
	sum = sum + C[j][0]
print ("Sum:\n%s" % sum)
