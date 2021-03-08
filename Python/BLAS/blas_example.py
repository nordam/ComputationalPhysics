#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from time import time
from scipy.linalg.blas import dgemm


M = 1700
N = 1800
K = 1900

A = np.arange(1, M*K + 1, dtype=np.float64).reshape(M, K)
B = np.arange(1, K*N + 1, dtype=np.float64).reshape(K, N)
C = np.empty((M, N))

tic = time()
for i in range(M):
    for j in range(N):
        C[i,j] = np.sum(A[i,:] * B[:,j])

toc = time()

print(f'Naïve matrix multiplication took {toc - tic} seconds')
print('Corners of C:')
print(C[0,0], C[-1,0], C[0,-1], C[-1,-1])

tic = time()
C = np.dot(A, B)
toc = time()

print(f'Call to np.dot() took {toc - tic} seconds')
print('Corners of C:')
print(C[0,0], C[-1,0], C[0,-1], C[-1,-1])

tic = time()
C = dgemm(alpha=1.0, a=A, b=B)
toc = time()

print(f'Call to sgemm() took {toc - tic} seconds')
print('Corners of C:')
print(C[0,0], C[-1,0], C[0,-1], C[-1,-1])


print(A.flags)
