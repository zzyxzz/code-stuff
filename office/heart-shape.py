import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0,2*np.pi,0.1)
##x = 2*np.cos(t) - np.cos(2*t)
##y = 2*np.sin(t) - np.sin(2*t)

y = 1 - np.cos(t)

plt.subplot(111, polar=True)
plt.plot(t,y)
plt.show()
