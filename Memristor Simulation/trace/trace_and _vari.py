import numpy as np
import pylab as plt
from cmemristor import memristor

##simulation parameters
dt = 0.025
T  = 60
##trace parameters
tau_p = 15  ##positive tau
tau_n = 15  ##negtive tau
time = np.arange(0, T + dt, dt)
delta_t = np.arange(-T, T + 0.05, 0.05)

A_p = 1     ##positive amplitude
A_n = 0.4    ##negative amplitude

##define trace   ##tx  = np.exp(-x / tau)

def kaishi():     ##time is spike start time
    area = np.zeros(len(delta_t))
    tx = np.zeros(len(time))
    for i, t in enumerate (delta_t):
        if delta_t[i] < 0:
            sign = -1
            tx = A_n * sign * np.exp((-time - abs(delta_t[i]))/tau_n)  ##get a whole trace based on one delta_t
        else:
            sign = 1
            tx = A_p * sign * np.exp((-time - abs(delta_t[i]))/tau_p)                                    
        area[i] = np.trapz(tx,time)   ## calculate the area under the trace
    return area

area1 = kaishi()

A_p = 1
A_n = 1
tau_p = 20
tau_n = 20

area2 = kaishi()

plt.figure()
plt.subplot(221)
plt.scatter( delta_t,  area2/max(abs(area2)), s = 0.5)
##plt.scatter( delta_t, -area/area[0], s = 0.5)
##plt.title('STDP Learning')
plt.xlabel(r'$\Delta t$',fontsize = 16)
plt.ylabel(r'$\xi (\Delta t)$',fontsize = 16)
plt.ylim([-1.2,1.2])
plt.grid(True)

plt.subplot(222)
plt.scatter( -delta_t,  area2/max(abs(area2)), s = 0.5)
##plt.scatter( delta_t, -area/area[0], s = 0.5)
##plt.title('STDP Learning')
plt.xlabel(r'$\Delta t$',fontsize = 16)
plt.ylabel(r'$\xi (\Delta t)$',fontsize = 16)
plt.ylim([-1.2,1.2])
plt.grid(True)

plt.subplot(223)
plt.scatter( delta_t,  area1/max(abs(area1)), s = 0.5)
##plt.scatter( delta_t, -area/area[0], s = 0.5)
##plt.title('STDP Learning')
plt.xlabel(r'$\Delta t$',fontsize = 16)
plt.ylabel(r'$\xi (\Delta t)$',fontsize = 16)
plt.ylim([-1.2,1.2])
plt.grid(True)

plt.show()
