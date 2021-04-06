#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time, sleep
import numpy as np
from mpi4py import MPI
sleep(100)

# Initialise MPI communicator
comm = MPI.COMM_WORLD()
MPI_rank = comm.Get_rank()
MPI_size = comm.Get_size()

print(f'This is rank: {rank}')


