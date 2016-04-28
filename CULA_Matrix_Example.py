import ctypes
from scipy import *
from scipy.linalg import *
import numpy as np
import sys
import csv
print "___________________________________________________________________________________________________"

N = 2
na = 2

libculaC=ctypes.CDLL('libcula_lapack.so',mode=ctypes.RTLD_GLOBAL)
libculaC.culaGetStatusString.restype=ctypes.c_char_p

info=libculaC.culaInitialize()


Anp = np.matrix(np.random.rand(na,na)) # 2x2 array

for a in Anp:
	print a
	
print "___________________________________________________________________________________________________"

Anp = Anp.astype(numpy.float32)
c_float_p = ctypes.POINTER(ctypes.c_float)
A1_p = Anp.ctypes.data_as(c_float_p)

B1 = np.matrix(np.random.rand(na,na)) # 2x2 array
for a in B1:
	print a
	
print "___________________________________________________________________________________________________"

B1 = B1.astype(numpy.float32)
B1_p = B1.ctypes.data_as(c_float_p)

X=np.matrix(2,)  # 2x0 array
X=X.astype(numpy.float32)
X_p =X.ctypes.data_as(c_float_p)

start = libculaC.time()
libculaC.culaSgesv(2,1,A1_p,2,X_p,B1_p,2)
finish = libculaC.time()
print 'time for solution is ', finish - start,'s'

buffer = numpy.core.multiarray.int_asbuffer(ctypes.addressof(X_p.contents), 8*2)
a = np.frombuffer(X_p) 
for a in a:
	print a 

libculaC.culaShutdown()
