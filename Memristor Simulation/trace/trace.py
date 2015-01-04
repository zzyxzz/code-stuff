import numpy as np
import pylab as plt
from cmemristor import memristor

##simulation parameters
dt = 0.05 ##0.025

##trace parameters
tau_p = 15  ##positive tau
tau_n = 15  ##negtive tau
time = np.arange(0, 60 + dt, dt)
delta_t = np.arange(-60, 60 + 0.05, 0.05)
area = np.zeros(len(delta_t))
A_p = 1     ##positive amplitude
A_n = 1#0.4    ##negative amplitude

##define trace   ##tx  = np.exp(-x / tau)

def kaishi():     ##time is spike start time
    tx = np.zeros(len(time))
    for i, t in enumerate (delta_t):
        if delta_t[i] < 0:
            sign = -1
            tx = A_n * sign * np.exp((-time - abs(delta_t[i]))/tau_n)  ##get a whole trace based on one delta_t
        else:
            sign = 1
            tx = A_p * sign * np.exp((-time - abs(delta_t[i]))/tau_p)                                    
        area[i] = np.trapz(tx,time)   ## calculate the area under the trace

kaishi()

plt.figure()
plt.scatter( delta_t,  area/max(abs(area)), s = 0.5)
##plt.scatter( delta_t, -area/area[0], s = 0.5)
##plt.title('STDP Learning')
plt.xlabel(r'$\Delta t$',fontsize = 20)
plt.ylabel(r'$\xi (\Delta t)$',fontsize = 20)
plt.ylim([-1.2,1.2])
plt.grid(True)

plt.show()
