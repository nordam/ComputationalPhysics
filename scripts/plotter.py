import re
import sys
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
# Get nicer looking plots than default
plt.style.use('bmh')

plt.figure(figsize = (12,6))
linewidth = 2
alpha = 0.9

for filename in sys.argv[1:]:
    # Get y-value from filename using regular expressions
    p = re.compile('results_([0-9.]*)\.txt')
    m = p.match(filename)
    y = float(m.group(1))
    # read X-values from text file
    X = np.loadtxt(filename)
    plt.plot(X[:,0], X[:,1], label = str(y), lw = linewidth, alpha = alpha)

plt.legend()
plt.savefig('trajectories.png')


