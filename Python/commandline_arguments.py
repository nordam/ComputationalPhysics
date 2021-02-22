#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from functions import euler, rk4, run_simulation

# Create an argument parser object
parser = argparse.ArgumentParser(description = 'Solve the ODE dx/dt = -x, for given initial value and given time')

# Define positional argument (mandatory argument)
parser.add_argument('x0', type = float, help = 'Initial value for ODE')
parser.add_argument('Tmax', type = float, help = 'Time to find solution  for')

# Define optional arguments
parser.add_argument('--dt', dest = 'dt', type = float, default = 0.1, help = 'Timestep to use in ODE solver')
parser.add_argument('--method', dest = 'method', default = 'rk4', choices = ['euler', 'rk4'], help = 'ODE method to use')

# Parse arguments, and create an object storing the results
args = parser.parse_args()

# We can access the arguments as properties on the args object
X0 = args.x0
Tmax = args.Tmax
dt = args.dt
# Choosing integrator based on input
if args.method == 'rk4':
    method = rk4
else:
    method = euler


# Define function for RHS of ODE
def f(x, t):
    return -x

# Run simulation
X = run_simulation(X0, Tmax, dt, f, method)

# Print result
print(f'Result: X({Tmax}) = {X}')
