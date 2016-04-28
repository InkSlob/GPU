import ctypes

N = 10
M = 10

libculaC=ctypes.CDLL("libcula_lapack.so")
libculaC.culaGetStatusString.restype=ctypes.c_char_p

info=libculaC.culaInitialize()

Atype = ctypes.c_float*(N*N)
A = Atype()
TAUtype = ctypes.c_float*N
TAU = TAUtype()

print A
print TAU

info = libculaC.culaSsyev(ctypes.c_int(M),ctypes.c_int(N),
    A,ctypes.c_int(N),TAU)

print info

libculaC.culaShutdown()
