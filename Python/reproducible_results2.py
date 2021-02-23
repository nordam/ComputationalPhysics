#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The aim of this program is to illustrate one possible strategy for making sure you can reproduce simulation results.

import numpy as np
from functions import rk4, trajectory

# These libraries will help us make a copy of the program file itself
import os
from shutil import copyfile
# This library will help us make a unique folder name
import uuid

# Create a unique folder
foldername = f'simulation_results_{uuid.uuid4().hex}'
os.mkdir(foldername)
# Copy the program file to that folder
# __file__ is a special variable that contains the name of the current file
copyfile(__file__, os.path.join(foldername, os.path.basename(__file__)))

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
    np.save(os.path.join(foldername, outputfilename), results)
