from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from memristor_hp_i import memristor as hpmr

dt = 0.0025
sim_time = 1
time = np.arange(0, sim_time+dt, dt)
sig = 5*(signal.square(2*np.pi*5*time) + 1)

mem = hpmr(sim_time, dt)
for i, t in enumerate(sig):
    if i > 0:
        mem.i[i] = t/mem.r[i-1]
        if t > 0:
            mem.q_i_t(i)
        else:
            mem.q[i] = mem.q[i-1]
    mem.w_q_t(i)  
    mem.r_q_t(i)
    mem.v_r_t(i)
    mem.phi_v_t(i)
    
plt.figure()

plt.subplot(211)
plt.plot(time, mem.w)
plt.xlabel('time')
plt.ylabel('MR')

plt.subplot(212)
plt.xlabel('time')
plt.ylabel('current')
#plt.plot(time, mem.i)
plt.plot(time,sig)
plt.ylim([-1,3])
plt.show()
