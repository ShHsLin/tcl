import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 10
c = 10
b = 8
m = 8
o = 9
n = 10
u = 32
v = 32
gflops = a*c*b*m*o*n*u*v*2/1e9
Ma = np.random.rand(2500**2).astype('f')
Mb = np.random.rand(2500**2).astype('f')
A = np.empty((u,v,o,m,n), order='f', dtype=np.float32)
B = np.empty((b,c,v,a,u), order='f', dtype=np.float32)
C = np.empty((m,o,c,b,n,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
timeTCL = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   tcl.tensorMult( alpha, A, "u,v,o,m,n", B, "b,c,v,a,u", beta, C, "m,o,c,b,n,a" )
   timeTCL = min(timeTCL, time.time() - s)
timeNP = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   C_ = np.einsum("uvomn,bcvau->mocbna", A, B)
   timeNP = min(time.time() - s, timeNP)
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
