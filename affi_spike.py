import numpy as np
import matplotlib.pyplot as plt

time = np.arange(0,55,0.01)
y = np.zeros(len(time))
x = np.zeros(len(time))

for i,t in enumerate(time):
    if t > 3:
        y[i] = -1;
    if t > 10:
        y[i] = -(1.0/40.0)*t + 5.0/4.0
    if t > 50:
        break
y[0] = 0

plt.figure()
plt.plot(time,y,linewidth = 3)
plt.plot(time, x, '--' ,linewidth = 1)
plt.ylim([-1.5, 1.5])
plt.xlim([-5, 55])
plt.xticks([ ])
plt.yticks([ ])
plt.show()
        
