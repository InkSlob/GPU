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

#Row major-normal form, but must be converted-('4 1;2 5')
Anp = np.matrix('4.0 2.0;1.0 5.0') #Column major
print "This is Anp: "
print Anp
print '___________END Anp______________'

#use ctypes to convert from Py to C
#2x2 matrix
Anp = Anp.astype(numpy.float32)  #astype is array type for ctype
c_float_p = ctypes.POINTER(ctypes.c_float)
A1_p = Anp.ctypes.data_as(c_float_p)
# 2x1 matrix
B1 = np.matrix('5.0 ;7.0')
print "This is B1"
print B1
print '__________________B1 END______________________'
B1 = B1.astype(numpy.float32)
B1_p = B1.ctypes.data_as(c_float_p)

X=np.empty([2])
X=X.astype(numpy.float32)
X_p =X.ctypes.data_as(c_float_p)
print "This is X"
print X
print '__________________X END______________________'

libculaC.culaSgesv(2,1,A1_p,2,X_p,B1_p,2)  #libculaC.culaSgesv

a = np.fromiter(B1_p, dtype=np.float32, count=2)
a = np.reshape(a,(-1,2))
print "The solution returning from Sgesv: "
print a
print "-----------------------Program End----------------------------"

libculaC.culaShutdown()
