import ctypes
from scipy import *
from scipy.linalg import *
import numpy as np
import sys
import csv

libculaC=ctypes.CDLL('libcula_lapack.so',mode=ctypes.RTLD_GLOBAL)
libculaC.culaGetStatusString.restype=ctypes.c_char_p

info=libculaC.culaInitialize()

def fileCov(na):
        rmean = zeros(na)
        y = zeros((na, na))
        with open('covMatrix.csv', 'r') as f1:
                reader = csv.reader(f1)
                i = 0
                for row in reader:
                        y[i] = np.array(row, float64)
                        i = i +1

        with open('rMean.csv', 'r') as f2:
                reader = csv.reader(f2)
                for row in reader:
                        rmean = np.array(row, float64)
        return rmean, y

def generateCov(na, ns):
        rmean = zeros(na)
        rvolat = zeros(na)
        for i in range(na):
                t1 = np.random.uniform(-7.0, 7.0)
                rmean[i] = t1
                rvolat[i] = math.fabs(t1)/7.0
        print rmean
        print rvolat
        z = zeros((na,ns))
        for j in range(na):
                r = np.random.normal(rmean[j], rvolat[j], ns)
                z[j] = r
        return rmean, np.cov(z)
na = 256
ns = 1000
na = 8
rmean, y = fileCov(na)
print "This is Y:"
print y
print "This is rmean:"
print rmean
y = y.astype(numpy.float32)
c_float_p = ctypes.POINTER(ctypes.c_float)
y_c=y.ctypes.data_as(c_float_p)
rmean = rmean.astype(numpy.float32)
rmean_c=rmean.ctypes.data_as(c_float_p)
X=array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
X=X.astype(numpy.float32)
X_p =X.ctypes.data_as(c_float_p)
libculaC.culaSgesv(8,1,y_c,8,X_p,rmean_c,8)
a = np.fromiter(rmean_c, dtype=np.float, count=8)
b= np.fromiter(X_p, dtype=np.float, count=8)
#floatList = [a[i] for i in range(9)]
for x in a:
	print x
for x in b:
	print b



