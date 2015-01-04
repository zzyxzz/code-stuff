from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

dt = 0.025
sim_time = 1
time = np.arange(0, sim_time+dt, dt)
sig = signal.square(2*np.pi*5*time) + 1


plt.xlabel('time')
plt.ylabel('current')
#plt.plot(time, mem.i)
plt.plot(time,sig)
plt.ylim([-1,3])
plt.show()
