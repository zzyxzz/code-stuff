
#########################################################################
#              This code intends to implement                           #
#   the switching dynamics model in paper "A ferroelectric memristor"   #
#   (the zones involved in the switching process may depend on voltage) #
#########################################################################


import numpy as np
import pylab as plt
from cmemristor_gai import stair_memristor
##unknown ##tau_n##  ##nucleation time depends on voltage
tau = [0.4,0.9,1.5]

##unknown   ##propagation time depends on voltage
tau_p = 1/10.0 

##unknown   ##the area of each zone normalized by total juntion area
si = [0.33, 0.34, 0.33]

#si10    = 1.0/9.0

def hfunc(t):
    if t >= 0:
        return 1
    else:
        return 0

time = np.arange(0,2+0.025,0.025) ##simulation time
s = np.zeros(len(time))
#mem = np.zeros(len(time))
for i,t in enumerate(time):
    if t < tau[1]:
        tau_n = tau[0]
        ht =  hfunc(t - tau_n)
        s[i] = 1.0 - si[0]*ht*(1.0 - np.tanh( - ((t-tau_n)/tau_p)**2.0 ) )
    elif t < tau[2]:
        tau_n = tau[1]
        ht =  hfunc(t - tau_n)
        s[i] = (1-si[0]) - si[1]*ht*(1.0 - np.tanh( - ((t-tau_n)/tau_p)**2.0 ) )
    else:
        tau_n = tau[2]
        ht =  hfunc(t - tau_n)
        s[i] = (1-si[0]-si[1]) - si[2]*ht*(1.0 - np.tanh( - ((t-tau_n)/tau_p)**2.0 ) )
    
##s the ratio ## down-to-up switching
ron  = 1.0/3.0
roff = 100.0        
mem  = ron*roff/(s*(ron-roff) + roff)
gmem = 1/mem
############################################
#             define state variable        #
#              ds/dt = f(s,V,t)            #
############################################
#ds/dt = (1-s)*(2/tau_p*((t-tau_n)/tau_p))

##########################
#V(t) = R(s,V,i)*i(t)
##########################

## Stimulus of memristor
m = stair_memristor(0.025, time)

for i,t in enumerate(time):
    if i >= 0:
        m.phi_t_pw(i,t)

plt.figure()
plt.plot(time,s)

plt.figure()
plt.plot(time,gmem,'-',label = 'staircase')
plt.plot(time,1/m.r,'--',label = 'ideal staircase')
plt.xlabel(r'$\varphi$',fontsize = 16)
plt.ylabel(r'$g(\varphi)$',fontsize = 16)
plt.ylim([0,3])
plt.legend(loc=4,ncol=1)
plt.show()
