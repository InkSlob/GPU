import ctypes
from scipy import *
from scipy.linalg import *
import numpy as np
import sys
import csv

N = 10
M = 10

libculaC=ctypes.CDLL("libcula_lapack.so")
libculaC.culaGetStatusString.restype=ctypes.c_char_p


#make a numpy array; you may use float32 or float64 dtypes
cat = np.array([[1,2],[3,4]])
cat = cat.astype(numpy.float32)
c_float_p = ctypes.POINTER(ctypes.c_float)
data_p = cat.ctypes.data_as(c_float_p)

#run PyCULA routine; print results
lamb = libculaC.culaSgesv(data_p)
print lamb

#shutdown PyCULA
libculaC.culaShutdown()