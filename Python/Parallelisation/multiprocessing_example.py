#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import numpy as np


def random_function(x):
    r = np.random.random()
    print(f'This is random_function, {x} = x, my random number is {r}')


if __name__ == '__main__':
    # List of inputs for which to run simulation
    parameters = np.arange(12)

    processes = []

    for x in parameters:
        # the function is defined in the file wait_function.py,
        # see comments above
        p = Process(target = random_function, args = (x, ))
        p.start()
        processes.append(p)

    # Wait for all copies to finish before proceeding.
    # p.join() does not return until the process is complete.
    for p in processes:
        p.join()
