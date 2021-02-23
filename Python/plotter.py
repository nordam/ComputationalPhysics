#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np

import sys

# This is the simplest way of reading a command line argument
result_filename = sys.argv[1]

# Use tuple unpacking to split into two arrays
X, T = np.load(result_filename)

# Read out a parameter from filename:
# Split the filename on _ and then on =
# (this is a bit hackety-hack)
for s in result_filename.split('_'):
    if s.startswith('dt'):
        dt = s.split('=')[-1]

plt.plot(X, T, label = f'Results, dt = {dt}')
plt.legend()
plt.xlabel('Time')
plt.ylabel('X')
plt.tight_layout()

# Save plot with same name as result file, except for file extension
plot_filename = result_filename.replace('npy', 'png')
plt.savefig(plot_filename)
