from scipy import *
from scipy.linalg import *
import numpy as np
import sys
import csv
import ctypes

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
#sys.exit()
np.random.seed(0)
#rmean, y = generateCov(na, ns)
A = zeros((na+2,na+2))
for i in range(na):
	for j in range(na):
		A[i][j] = y[i][j]
	A[i][na] = -rmean[i]  
	A[i][na+1] = -1.0
for j in range(na):
	A[na][j] = rmean[j]
	A[na+1][j] = 1.0
  
x = zeros(na+2)
b = zeros(na+2)
b[na] = 57.64
b[na+1] = 1.0
print "This is A: "
print A
print "This is b: "
print b

# The 10x10 matrix
#input("Press Enter to continue...")
A_t = A
A_t = A_t.astype(numpy.float32) #float32
c_float_p = ctypes.POINTER(ctypes.c_float)
A1_p = A_t.ctypes.data_as(c_float_p)
# The 10x1 matrix
x1= np.empty([na+2])
x1= x1.astype(numpy.float32)
X_p = x1.ctypes.data_as(c_float_p)
# The 10x1 matrix with covariance
b_t=b.T
b_t = b_t.astype(numpy.float32)
b1_p = b_t.ctypes.data_as(c_float_p)

x = solve(A, b)

libculaC.culaSgesv(10,1,A1_p,10,X_p,b1_p,10)
a = np.fromiter(b1_p, dtype=np.float32, count=10)
print a
print "THIS IS X from solver:"
print x
print "x is over"
ym = np.matrix(y)
xm = np.matrix(a[0:na])  #x changed to a
print "This is ym: "
print ym
print "This is xm: "
print xm
print "This is sqrt(xm * ym * xm.T): "
print sqrt(xm * ym * xm.T)
sum = 0.0
for j in range(na):
	sum = sum + a[j]  #x changed to a
print sum


libculaC.culaShutdown()
