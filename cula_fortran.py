from scipy import *
from scipy.linalg import *
import numpy as np
import sys
import csv
import ctypes

libculaC=ctypes.CDLL('libcula_lapack.so',mode=ctypes.RTLD_GLOBAL)
libculaC.culaGetStatusString.restype=ctypes.c_char_p

info=libculaC.culaInitialize()


A = np.matrix('1.80 2.88 2.05 -0.89;5.25 -2.95 -0.95 -3.80;1.58 -2.69 -2.90 -1.04;-1.11 -0.66 -0.59 0.80')
A = np.reshape(A,(4,4),order='F')
b = np.matrix('9.52;24.35;0.77;-6.22')
b = np.reshape(b,(4,1),order='F')

A_t = A
A_t = A_t.astype(numpy.float32) #float32
c_float_p = ctypes.POINTER(ctypes.c_float)
c_integer_p = ctypes.POINTER(ctypes.c_int)
A1_p = A_t.ctypes.data_as(c_float_p)
# The 10x1 matrix
x1= np.int_([0,0,0,0])
X_p = x1.ctypes.data_as(c_integer_p)
# The 10x1 matrix with covariance
b_t=b
b_t = b_t.astype(numpy.float32)
b1_p = b_t.ctypes.data_as(c_float_p)

print "A: ", A
print "b: ", b
print "then the answer is: "
libculaC.culaSgesv(4,1,A1_p,4,X_p,b1_p,4)
a = np.fromiter(b1_p, dtype=np.float32, count=4)
print a

pyX = solve(A, b)
print "Python solver: \n", pyX

libculaC.culaShutdown()
