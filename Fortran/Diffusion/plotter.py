# Import numpy and matplotlib, and use jupyter magic to
# get plots directly in notebook
import sys
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
# Get nicer looking plots than default
plt.style.use('bmh')

U = np.loadtxt(sys.argv[1])
X = np.linspace(-5, 5, len(U))
plt.plot(X, U)
plt.ylim(-0.2, 1.2)
plt.savefig('diffusion.png')
