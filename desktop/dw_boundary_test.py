import numpy as np
import matplotlib.pyplot as plt

time = np.arange(-5,5,0.01)


q = np.exp(time/15)

w = 4/(np.exp(-4*time) + 4)

plt.plot(time, w)
plt.show()
