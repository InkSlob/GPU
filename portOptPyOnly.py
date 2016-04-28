from scipy import *
from scipy.linalg import *
import numpy as np
import sys
import csv
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
x = solve(A, b)
print "THIS IS X from solver:"
print x
print "x is over"
ym = np.matrix(y)
xm = np.matrix(x[0:na])
print "This is ym: "
print ym
print "This is xm: "
print xm
print "This is sqrt(xm * ym * xm.T): "
print sqrt(xm * ym * xm.T)
sum = 0.0
for j in range(na):
	sum = sum + x[j]
print sum