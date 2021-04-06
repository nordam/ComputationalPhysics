#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import time, sleep
import numpy as np
from mpi4py import MPI



def FTCS(C_now, D, dt, dx):
    # One iteration with the FTCS method
    # Interior points only
    alpha = D*dt/dx**2
    C_now[1:-1, 1:-1] = C_now[1:-1, 1:-1] + alpha*(
         C_now[2:  , 1:-1]
        +C_now[ :-2, 1:-1]
        +C_now[1:-1, 2:  ]
        +C_now[1:-1,  :-2]
        -4*C_now[1:-1, 1:-1]
    )
    return C_now



# Initialise MPI communicator
comm = MPI.COMM_WORLD
MPI_rank = comm.Get_rank()
MPI_size = comm.Get_size()

if MPI_rank == 0:
    tic = time()

# Numerical parameters
Nx, Ny = 1024, 512
Xmin, Xmax = 0, 2
Ymin, Ymax = 0, 1
Tmax = 5
dt = 0.001

# Diffusivity
D = 0.0009

# Global coordinates
xc, dx = np.linspace(Xmin, Xmax, Nx, retstep = True)
yc, dy = np.linspace(Ymin, Ymax, Ny, retstep = True)

# Check stability condition for this method
assert D*dt/dx**2 < 0.25

# Infer local coordinates from rank, splitting the array along the x-axis only
cells_per_rank = int(Nx/MPI_size)

if MPI_size > 1:
    # Treat first and last rank separately
    if MPI_rank == 0:
        x_local = xc[ : cells_per_rank + 1]
    elif MPI_rank == MPI_size - 1:
        x_local = xc[MPI_rank * cells_per_rank - 1 : ]
    else:
        x_local = xc[MPI_rank * cells_per_rank - 1 : (1+MPI_rank)*cells_per_rank + 1]
else:
    x_local = xc

y_local = yc

print(f'This is rank: {MPI_rank} of {MPI_size}. Local x-axis is from {x_local[0]} to {x_local[-1]}')
sys.stdout.flush()



# Initial concentration (gaussian)
x0, y0 = 1.0, 0.5
sx, sy = 0.05, 0.05

# local grid points
gridy, gridx = np.meshgrid(y_local, x_local)
# Create concentration field for local cells only
C0 = np.exp(-(gridx - x0)**2/(2*sx**2) - (gridy-y0)**2/(2*sy**2))

# Work array
C = C0.copy()


# Loop over time
Nt = int(Tmax/dt)
for i in range(Nt):
    # Update interior points
    C = FTCS(C, D, dt, dx)

    # Only communicate if there is more than one rank
    if MPI_size > 1:
        # Exchange halo with neighbours
        # First set up non-blocking receives
        if MPI_rank == 0:
            # Set up non-blocking receive from the right
            comm.Irecv(C[-1,:], source = MPI_rank + 1)
        elif MPI_rank == MPI_size - 1:
            # Set up non-blocking receive from the left
            comm.Irecv(C[ 0,:], source = MPI_rank - 1)
        else:
            # Set up non-blocking receive from both the left and the right
            comm.Irecv(C[ 0,:], source = MPI_rank - 1)
            comm.Irecv(C[-1,:], source = MPI_rank + 1)

        # Then, set up blocking sends
        if MPI_rank == 0:
            # Set up blocking send to the right
            comm.Send(C[-2,:], dest = MPI_rank + 1)
        elif MPI_rank == MPI_size - 1:
            # Set up blocking send to the left
            comm.Send(C[ 1,:], dest = MPI_rank - 1)
        else:
            # Set up non-blocking send to both the left and the right
            comm.Send(C[ 1,:], dest = MPI_rank - 1)
            comm.Send(C[-2,:], dest = MPI_rank + 1)

        comm.Barrier()

print(f'This is rank: {MPI_rank} of {MPI_size}, finished computations')
sys.stdout.flush()

# Finally, gather results on rank 0, and store to file
if MPI_rank == 0:
    C0_global = np.zeros((MPI_size, cells_per_rank, Ny))
    C_global = np.zeros((MPI_size, cells_per_rank, Ny))
else:
    C0_global = None
    C_global = None

# Create a view of the local array that excludes boundary cells
if MPI_rank == 0:
    C0_local = C0[:-1, :]
    C_local = C[:-1, :]
elif MPI_rank == MPI_size -1:
    C0_local = C0[1:, :]
    C_local = C[1:, :]
else:
    C0_local = C0[1:-1, :]
    C_local = C[1:-1, :]

# Only communicate if there is more than one rank
if MPI_size > 1:
    # Collective communication
    comm.Gather(C_local, C_global, root = 0)
    comm.Gather(C0_local, C0_global, root = 0)
else:
    # If there is only one rank, store the entire array
    C0_global = C0
    C_global = C

if MPI_rank == 0:
    np.save('C0_MPI.npy', C0_global.reshape(Nx, Ny))
    np.save('C_MPI.npy', C_global.reshape(Nx, Ny))
    toc = time()
    print(f'Simulation took {toc - tic:.5f} seconds')

