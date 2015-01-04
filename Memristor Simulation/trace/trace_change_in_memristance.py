import numpy as np
import pylab as plt
from cmemristor import memristor

##simulation parameters
dt = 0.025
T  = 80
##trace parameters
tau_p = 16  ##positive tau
tau_n = 16  ##negtive tau
time = np.arange(0, T + dt, dt)
delta_t = np.arange(-T, T + 0.05, 0.05)

A_p = -1     ##positive amplitude
A_n = -1  ##0.4    ##negative amplitude

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

A_p = 0.5
A_n = 0.5
tau_p = 10
tau_n = 20

area2 = kaishi()

##########cal hp memristance##########
Ron = 10
Roff = 160
D = 1
#Rmem = Ron*w/D + Roff*(1-w/D)

Rm = -(Ron-Roff)*(area1/D)

Rm2 = -(Ron-Roff)*(area2/D)

ds = 1/(1 + np.exp(-(0.2 + area1/50)*20 +10)) - 1/(1 + np.exp(-0.2*20 + 10))

###########################

plt.figure(figsize=(12,5),dpi=100)
plt.subplot(121)
plt.scatter(delta_t,Rm/max(abs(Rm)), s = 0.5)
plt.grid(True)
plt.ylim([-1.2,1.2])
plt.xlabel(r'$\Delta t$', fontsize = 16)
plt.ylabel(r'$\Delta Rmem$', fontsize = 16)
plt.title('(a)')

plt.subplot(122)
plt.scatter(delta_t,Rm2/max(abs(Rm2)), s = 0.5)
plt.grid(True)
plt.ylim([-1.2,1.2])
plt.xlabel(r'$\Delta t$', fontsize = 16)
plt.ylabel(r'$\Delta Rmem$', fontsize = 16)
plt.title('(b)')
plt.tight_layout()

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
