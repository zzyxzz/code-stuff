
import numpy as np
import pylab as plt
##from cmemristor_gai import stair_memristor
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

time = np.arange(0,4+0.025,0.025) ##simulation time

s = np.zeros(len(time))
ds = np.zeros(len(time))

for i,t in enumerate(time):
    s[i] =  1/(1+np.exp(t*12 - 10))
    ds[i] = -4 * np.exp(t*4 - 10)/((1 + np.exp(t*4 - 10))**2)
    
plt.figure()
plt.subplot(211)
plt.plot(time,s)
plt.grid(True)
#plt.xlim([0,10])
plt.subplot(212)
plt.plot(time, ds)
plt.grid(True)
plt.show()
