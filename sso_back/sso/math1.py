import math
import numpy as np

for A in np.arange(0, 400, 0.1):
    for B in np.arange(0, 400, 0.1):
        if 149 * A + 284 * B == 117680:
            print("AB分别等于{},{}".format(A, B))