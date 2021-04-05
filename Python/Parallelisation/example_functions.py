#!/usr/bin/env python
# -*- coding: utf-8 -*-

def wait_function(x):
    import time
    time.sleep(3)
    print(f'This is wait_function, x = {x}, sleeping a few seconds...')
    return x**2

def random_function(x):
    import numpy as np
    r = np.random.random()
    print(f'This is random_function, x = {x}, my random number is {r}')
    return x**2

