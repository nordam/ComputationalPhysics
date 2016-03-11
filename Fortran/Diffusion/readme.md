# Diffusion with OpenMP

The file `diffusion.f90` contains a simple implementation of the explicit forward scheme for PDEs presented in the lecture on March 11. It uses operations on elements of a vector instead of matrix-vector multiplication. This implementation lends itself very nicely to shared memory parallelisation, as all elements in the next timestep are independent of each other, depending only on the values from the current timestep. The two comments starting with `!$OMP` are so-called compiler directives, telling the compiler to try to parallelise the loop contained within.

Compile the code, run the program an make the plot like this:

```
gfortran -fopenmp -o diffusion diffusion.f90
time OMP_NUM_THREADS=1 ./diffusion > u.txt
python plotter.py u.txt
```

Try different values of `OMP_NUM_THREADS`. On my machine, it runs in about 20 seconds with 1 thread, and 13.5 seconds with 2. Note that this is a tiny problem, which means that the overhead of introducing parallelisation is significant compared to the actual work involved. If you increas the simulation time by increasing `Nx` (and thus decreasing `dt`), or by increasing `T`, you should see greater speedup.

Note also that I purposefully compile without optimisation flags. If I compile with `-O3`, the time goes down to 3.5 seconds for 1 thread, and 5.2 seconds for 2 threads, which sort of ruins the demonstration of OpenMP. The take-home message is:

* OpenMP can sometimes give you a decent speedup with minimal effort.
* Parallelisation does not always work perfectly, especially for small problems.

