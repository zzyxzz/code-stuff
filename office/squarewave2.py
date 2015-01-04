from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from cmemristor import memristor as mr

dt = 0.0025
sim_time = 1
time = np.arange(0, sim_time+dt, dt)
sig = signal.square(2*np.pi*10*time) + 1

mem = mr(dt, time)

#mem.i = sig
for i, t in enumerate(sig):
    if i > 0:
        if t > 0:
            mem.q_t(i, t)
        else:
            mem.q[i] = mem.q[i-1]
    mem.phi_t_cubic_poly(i)
    mem.v_t(i)
    mem.r_t(i)
    
plt.figure()

plt.subplot(211)
plt.plot(time, mem.r)
plt.xlabel('time')
plt.ylabel('MR')

plt.subplot(212)
plt.xlabel('time')
plt.ylabel('current')
#plt.plot(time, mem.i)
plt.plot(time,sig)
plt.ylim([-1,3])
plt.show()
