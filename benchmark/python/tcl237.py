import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 12
c = 12
b = 12
d = 8
m = 12
n = 8
u = 128
gflops = a*c*b*d*m*n*u*2/1e9
Ma = np.random.rand(2500**2).astype('f')
Mb = np.random.rand(2500**2).astype('f')
A = np.empty((u,a,c,d,b), order='f', dtype=np.float32)
B = np.empty((n,m,u), order='f', dtype=np.float32)
C = np.empty((d,m,c,a,n,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
timeTCL = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   tcl.tensorMult( alpha, A, "u,a,c,d,b", B, "n,m,u", beta, C, "d,m,c,a,n,b" )
   timeTCL = min(timeTCL, time.time() - s)
timeNP = 1e100
for i in range(5):
   Mb = Ma *1.1 +  Mb #trash cache
   s = time.time()
   C_ = np.einsum("uacdb,nmu->dmcanb", A, B)
   timeNP = min(time.time() - s, timeNP)
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC
