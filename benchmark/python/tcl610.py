import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 3240
u = 54
v = 54
m = 64
n = 54
gflops = a*u*v*m*n*2/1e9
Ma = np.random.rand(2500**2).astype('f')
Mb = np.random.rand(2500**2).astype('f')
A = np.empty((m,n,v,u), order='f', dtype=np.float32)
B = np.empty((a,u,v), order='f', dtype=np.float32)
C = np.empty((m,a,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
timeTCL = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   tcl.tensorMult( alpha, A, "m,n,v,u", B, "a,u,v", beta, C, "m,a,n" )
   timeTCL = min(timeTCL, time.time() - s)
timeNP = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   C_ = np.einsum("mnvu,auv->man", A, B)
   timeNP = min(time.time() - s, timeNP)
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
