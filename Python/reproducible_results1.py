#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The aim of this program is to illustrate one possible strategy for making sure you can reproduce simulation results.

import numpy as np
from functions import rk4, trajectory

# RHS of ODE
def f(x, t):
    return -0.1*x

# Define parameters (typically these would come from the command line, or a file, or something)
T0 = 0
Tmax = 100
X0 = 10

# Run for a few different timesteps
for dt in [0.01, 0.1, 1]:
    # Run simulation
    X, T = trajectory(X0, T0, Tmax, dt, f, rk4)
    # Merge results into one array
    # (more convenient with a single file in this case)
    results = np.array((X, T))

    # Save results with informative filename
    outputfilename = f'results_Tmax={Tmax}_dt={dt}_X0={X0}.npy'
    np.save(outputfilename, results)
