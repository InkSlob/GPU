import ctypes
from scipy import *
from scipy.linalg import *
import numpy as np
import sys
import csv
print "___________________________________________________________________________________________________"

libculaC=ctypes.CDLL('libcula_lapack.so',mode=ctypes.RTLD_GLOBAL)
libculaC.culaGetStatusString.restype=ctypes.c_char_p

info=libculaC.culaInitialize()

na = 5

#Row major-normal form, but must be converted-('4 1;2 5')
AAA = np.zeros([na,na])
print "checking 0s in AAA:"
print AAA

Anp = np.matrix([[1.80, 2.88, 2.05, -0.89, 0.236],[5.25, -2.95, -0.95, -3.80, 0.2365],[1.58, -2.69, -2.90, -1.04, 2.36],[-1.11, -0.66, -0.59, 0.80, -3.65],[-3.11, -2.66, -0.29, 1.80, -1.65]]) #Column major

print "This is Anp: "
print Anp
print '___________END Anp______________'

for i in range(na):
    for j in range(na):
	    AAA[i,j] = Anp[j,i]

print "Anp reshaped as AAA: "
print AAA
pyA = Anp


#use ctypes to convert from Py to C
#2x2 matrix
Anp = AAA
Anp = Anp.astype(numpy.float32)  #astype is array type for ctype
c_float_p = ctypes.POINTER(ctypes.c_float)
A1_p = Anp.ctypes.data_as(c_float_p)
# 2x1 matrix
B1 = np.matrix([[9.52],[24.35],[0.77],[-6.22],[9.8]])
pyB1 = B1
print "This is B1"
print B1
print '__________________B1 END______________________'
B1 = B1.astype(numpy.float32)
B1_p = B1.ctypes.data_as(c_float_p)

X=np.zeros(na)
X=X.astype(numpy.float32)
X_p =X.ctypes.data_as(c_float_p)
print "This is X"
print X
print '__________________X END______________________'

libculaC.culaSgesv(na,1,A1_p,na,X_p,B1_p,na)  #libculaC.culaSgesv

a = np.fromiter(B1_p, dtype=np.float32, count=na)
print "The solution returning from Sgesv: "
print a
print "a matrix  after transpose"
print pyA.T
print "Python Solver Version"
pyX = solve(pyA, pyB1)
print pyX
print "-----------------------Program End----------------------------"

libculaC.culaShutdown()
