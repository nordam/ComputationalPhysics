#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The forward Euler method
def euler(x, t, h, f):
    # x is coordinates (as a vector)
    # h is timestep
    # f(x, t) is a function that returns the derivative
    # "Slopes"
    k1  = f(x,           t)
    # Update time and position
    x_  = x + h*k1
    return x_

# 4th-order Runge-Kutta
def rk4(x, t, h, f):
    # x is coordinates (as a vector)
    # h is timestep
    # f(x) is a function that returns the derivative
    # "Slopes"
    k1  = f(x,          t)
    k2  = f(x + k1*h/2, t + h/2)
    k3  = f(x + k2*h/2, t + h/2)
    k4  = f(x + k3*h,   t + h)
    # Update time and position
    x_  = x + h*(k1 + 2*k2 + 2*k3 + k4)/6
    return x_

def run_simulation(X, Tmax, h, f, integrator):
    # Number of timesteps
    Nt   = int((Tmax) / h)
    # Loop over timesteps
    t = 0
    for i in range(Nt+1):
        # Make sure the last step stops exactly at Tmax
        h  = min(h, Tmax - t)
        # Calculate next position
        X = integrator(X, t, h, f)
        # Increment time
        t += h
    return X
