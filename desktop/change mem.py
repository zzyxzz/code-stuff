import numpy as np
import pylab as plt
#from cmemristor_gai import stair_memristor
##unknown ##tau_n##  ##nucleation time depends on voltage
tau = [0.2,25,50]

##unknown   ##propagation time depends on voltage
tau_p = 10 

##unknown   ##the area of each zone normalized by total juntion area
si = [0.3, 0.3, 0.4]


#si10    = 1.0/9.0

def hfunc(t):
    if t >= 0:
        return 1
    else:
        return 0

time = np.arange(0,60+0.1,0.1) ##simulation time
s = np.zeros(len(time))

dw = -5*10*(np.exp(-60/10) - np.exp(-time/10))
#dw = 48 - (time - 12*((time/60)**5))
t0 = 10

#mem = np.zeros(len(time))
for i,t in enumerate(dw):
    if (t + t0) < tau[1]:
        tau_n = tau[0]
        ht =  hfunc(t + t0 - tau_n)
        s[i] = 1.0 - si[0]*ht*(1.0 - np.exp( - ((t+t0-tau_n)/tau_p)**2.0 ) )
    elif (t + t0) < tau[2]:
        tau_n = tau[1]
        ht =  hfunc(t + t0 - tau_n)
        s[i] = (1-si[0]) - si[1]*ht*(1.0 - np.exp( - ((t+t0-tau_n)/tau_p)**2.0 ) )
    else:
        tau_n = tau[2]
        ht =  hfunc(t + t0 - tau_n)
        s[i] = (1-si[0]-si[1]) - si[2]*ht*(1.0 - np.exp( - ((t+t0-tau_n)/tau_p)**2.0 ) )
    
##s the ratio ## down-to-up switching
ron  = 1.0#/3.0
roff = 40.0        
mem  = ron*roff/(s*(ron-roff) + roff)
gmem = 1/mem

###################
##simulation parameters
dt = 0.025   ##steps

##trace parameters
tau = 20           ##larger tau, longer trace
#time = np.arange(0, 60 + dt, dt)
A = 1          ## amplitude

##trace
def trace(det):
    tx = np.zeros(len(time))
    for i ,t in enumerate(time):
        if t >= det:
            tx[i] = A* np.exp((-t+det)/tau)
    return tx

## cal the trace
tx1 = trace(0)

####################

plt.figure()
plt.plot(time, tx1,'r--', -time, -tx1, 'r--', linewidth = 2)
#plt.plot(time,mem)
plt.scatter(time,(5-mem)/max(5-mem),s=2)
plt.scatter(-time,-(5-mem)/max(5-mem),s=2)
plt.grid(True)
plt.xlabel(r'$\Delta t$',fontsize = 16)
plt.ylabel(r'$\xi(\%)$',fontsize = 16)
plt.xlim([-61,61])
plt.ylim([-1.1,1.1])

plt.figure()
plt.plot(-time,-1+s)
plt.show()
