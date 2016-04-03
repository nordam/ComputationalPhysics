# MPI example

The file `jacobi.f90` contains a simple implementation of a solver for the Laplace or Poisson equation. It keeps two matrices in memory, and uses the current step to calculate a better approximation of a solution for the next step. This is relatively straightforward to parallelise with ghost cells.

Compile the code and run the program like this (you need to have MPI and a fortran compiler installed):

```
mpif90 -O3 -o jacobi jacobi.f90
mpirun -np 4 jacobi
```

MPI can be used both on a single machine, and on several machines over network. It's perfectly possible to run an MPI job with more processes than you have cores, for testing purposes.
