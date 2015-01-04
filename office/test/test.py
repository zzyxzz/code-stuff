import numpy as np
import matplotlib.pyplot as plt

time = np.arange(0,3,0.01)

s = np.zeros(len(time))
alpha= -2

for i,x in enumerate(time):
    s[i] = 1/(1+np.exp(6*x-9))

plt.figure()
plt.plot(time,s)
plt.grid(True)
plt.show()
