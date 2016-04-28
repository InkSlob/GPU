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
print "--- End A ---"	

# declare a matrix to hold transposed A
A_t = zeros((na+2,na+2))
for i in range(na+2):
    for j in range(na+2):
	    A_t[i][j] = A[j][i]

print "A transposed as A_t: "
print A_t 

A_t = A_t.astype(numpy.float32)
c_float_p = ctypes.POINTER(ctypes.c_float)
A1_p = A_t.ctypes.data_as(c_float_p)

x = zeros(na)
b = zeros(10)


b[na] = 57.64
b[na+1] = 1.0
print "THIS IS b:  "
print b
print "---- END ----"
print "THIS IS x before solver:  "
print x
print "---- END ----"
Xpy = zeros(na)
x = x.astype(numpy.float32)
x_p = x.ctypes.data_as(c_float_p) # to receive answer

b = b.astype(numpy.float32)
b_p = b.ctypes.data_as(c_float_p) # calculated off of

Xpy = solve(A, b)
#Sgesv(n,nrhs,a,lda,ipiv,b,ldb)
# solving A * X = B where A = A, X = b, and B = x in my notation
#1 n = number of linear equations
#2 nrhs = number of columns of the matrix B
#3 a = pointer to matrix A1_p
#4 lda = leading dimension of the array A.
#5 ipiv = an int array, output, with dimension N, defines permutation matrix
#6 b = pointer input/output, dimension nrhs, matrix b
#7 lbd = int as input is leading dimension of the array b
libculaC.culaSgesv(10,1,A1_p,10,x_p,b_p,10)
print "LibCULA SGESV: "
a = np.fromiter(b_p, dtype=np.float32, count=10)
print a

print "This is python solver: "
print Xpy
#for xx in xx:
  #print xx 

#ym = np.matrix(y)
#ym = ym.astype(numpy.float32)
#ym_p = ym.A.ctypes.data_as(c_float_p)

#xm = np.matrix(xx[0:na])
#print xm
#print sqrt(xm * ym * xm.T)
#sum = 0.0
#for j in range(na):
#	sum = sum + x[j]
#print sum

libculaC.culaShutdown()
