import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 32
b = 30
m = 30
o = 30
n = 30
u = 30
v = 32
gflops = a*b*m*o*n*u*v*2/1e9
Ma = np.random.rand(2500**2).astype('f')
Mb = np.random.rand(2500**2).astype('f')
A = np.empty((a,b,u,v), order='f', dtype=np.float32)
B = np.empty((v,n,u,o,m), order='f', dtype=np.float32)
C = np.empty((a,o,n,b,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
timeTCL = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   tcl.tensorMult( alpha, A, "a,b,u,v", B, "v,n,u,o,m", beta, C, "a,o,n,b,m" )
   timeTCL = min(timeTCL, time.time() - s)
timeNP = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   C_ = np.einsum("abuv,vnuom->aonbm", A, B)
   timeNP = min(time.time() - s, timeNP)
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
