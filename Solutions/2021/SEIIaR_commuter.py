#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numba import jit

@jit(nopython = True)
def SEIIaR_commuter_Nsteps(population, Nsteps, dt):
    # Hard-coding model parameters here
    beta=0.55
    f = np.array([0.6, 0.4]) # f_s and f_a
    r = np.array([1.0, 0.1]) # r_s and r_a
    tau_E = 3.0
    tau_I = 7.0
    # Calculate those probabilities that
    # do not depend on the other variables
    pEI, pEIa = f*(1 - np.exp(-dt/tau_E))
    pIR = 1 - np.exp(-dt/tau_I)
    # Number of towns
    Ntowns = population.shape[0]

    for i in range(Ntowns):
        for n in range(Nsteps):
            X = np.sum(population[i,:,:], axis = 0)
            # Transition from susceptible to exposed
            pSE = 1 - np.exp(-dt*beta*(np.sum(r*X[2:4]))/np.sum(X))
            for j in range(Ntowns):
                # Unpack variables for convenience
                S, E, I, Ia, R = population[i,j,:]
                # If (E + I + Ia) == 0 and pSE = 0, nothing will happen, so do nothing
                # (this saves a fair bit of simulation time in problem 2E)
                if ((E + I + Ia) > 0) or ((pSE > 0) and (S > 0)):
                    S2E = np.random.binomial(S, pSE)
                    E2I, E2Ia, _ = np.random.multinomial(E, (pEI, pEIa, 1-pEI-pEIa))
                    I2R = np.random.binomial(I, pIR)
                    Ia2R = np.random.binomial(Ia, pIR)
                    # Calculate new values
                    S  = S  - S2E
                    E  = E  + S2E  - E2I - E2Ia
                    I  = I  + E2I  - I2R
                    Ia = Ia + E2Ia - Ia2R
                    R  = R  + I2R  + Ia2R
                    population[i,j,:] = (S, E, I, Ia, R)
    return population


@jit(nopython = True)
def SEIIaR_commuter_one_day(population, dt):
    # Calculate number of timesteps in a day
    Nsteps = int(1/dt)
    # Confirm that the number of steps is even,
    # otherwise adjust timestep to correct
    if Nsteps % 2 != 0:
        Nsteps = Nsteps + 1
        dt = 1/Nsteps
    # Loop over all the daytime steps
    population = SEIIaR_commuter_Nsteps(population, Nsteps//2, dt)
    # Transpose matrix...
    population = np.transpose(population, axes = (1, 0, 2))
    # ...then loop over all the nighttime steps
    population = SEIIaR_commuter_Nsteps(population, Nsteps//2, dt)
    # Transpose back, then return
    population = np.transpose(population, axes = (1, 0, 2))
    return population


@jit(nopython = True)
def run_SEIIaR_commuter(population, Ndays, dt):
    history = np.zeros((population.shape[0], 5, int(Ndays)), dtype = np.int64)
    history[:,:,0] = np.sum(population, axis = 1)
    t = 0
    for i in range(1, Ndays):
        population = SEIIaR_commuter_one_day(population, dt)
        history[:,:,i] = np.sum(population, axis = 1)
    return history
