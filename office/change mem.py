import numpy as np
import pylab as plt
#from cmemristor_gai import stair_memristor
##unknown ##tau_n##  ##nucleation time depends on voltage
tau = [0.2,0.9,1.5]

##unknown   ##propagation time depends on voltage
tau_p = 1/1.0 

##unknown   ##the area of each zone normalized by total juntion area
si = [0.33, 0.34, 0.33]


#si10    = 1.0/9.0

def hfunc(t):
    if t >= 0:
        return 1
    else:
        return 0

time = np.arange(0,60+0.01,0.01) ##simulation time
s = np.zeros(len(time))

dw = -1*10*(np.exp(-60/10) - np.exp(-time/10))
t0 = 0.03

#mem = np.zeros(len(time))
for i,t in enumerate(time):
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
ron  = 1.0/3.0
roff = 40.0        
mem  = ron*roff/(s*(ron-roff) + roff)
gmem = 1/mem

plt.figure()
plt.plot(time,mem)
plt.xlim([0,2])
#plt.ylim([0,roff+1])
plt.show()
