from cmemristor_gai import stair_memristor
import numpy as np
import pylab as plt
from scipy.signal.waveforms import square
##from cmemristor_gai import stair_memristor
##unknown ##tau_n##  ##nucleation time depends on voltage
tau = [0.4, 0.9, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]

##unknown   ##propagation time depends on voltage
tau_p = 1/10.0 

##unknown   ##the area of each zone normalized by total juntion area
si = [0.0004, 0.0005, 0.0006, 0.0006, 0.0008, 0.0009, 0.0011, 0.0014, 0.0018, 0.0024, 0.0033, 0.0051, 0.0084, 0.0167, 0.0503, 0.9057]
#si10    = 1.0/9.0

def hfunc(t):
    if t >= 0:
        return 1
    else:
        return 0

time = np.arange(0,15+0.025,0.025) ##simulation time

s = np.zeros(len(time))
ds = np.zeros(len(time))

dt = 0.025
i = 0.025*(1.0*square(1.0*m.ts, duty=0.09)+1.0)

for i,t in enumerate(time):
    #s[i] =  1/(1+np.exp(t*12 - 10))
    #ds[i] = -4 * np.exp(t*4 - 10)/((1 + np.exp(t*4 - 10))**2)
    if t*20 <= 14:
        s[i] = (1 - 1.0/16)  + (1.0/16)/(1+np.exp(t*20 -10))
    elif t*20 <= 28:
        s[i] = (1 - 2.0/16) + (1.0/16)/(1+np.exp((t*20 - 24)))
    elif t*20 <= 42:
        s[i] = (1 - 3.0/16) + (1.0/16)/(1+np.exp((t*20 - 38)))
    elif t*20 <= 56:
        s[i] = (1 - 4.0/16) + (1.0/16)/(1+np.exp((t*20 - 52)))
    elif t*20 <= 70:
        s[i] = (1 - 5.0/16) + (1.0/16)/(1+np.exp((t*20 - 66)))
    elif t*20 <= 84:
        s[i] = (1 - 6.0/16) + (1.0/16)/(1+np.exp((t*20 - 80)))
    elif t*20 <= 98:
        s[i] = (1 - 7.0/16) + (1.0/16)/(1+np.exp((t*20 - 94)))
    elif t*20 <= 112:
        s[i] = (1 - 8.0/16) + (1.0/16)/(1+np.exp((t*20 - 108)))
    elif t*20 <= 126:
        s[i] = (1 - 9.0/16) + (1.0/16)/(1+np.exp((t*20 - 122)))
    elif t*20 <= 140:
        s[i] = (1 - 10.0/16) + (1.0/16)/(1+np.exp((t*20 - 136)))
    elif t*20 <= 154:
        s[i] = (1 - 11.0/16) + (1.0/16)/(1+np.exp((t*20 - 150)))
    elif t*20 <= 168:
        s[i] = (1 - 12.0/16) + (1.0/16)/(1+np.exp((t*20 - 164)))
    elif t*20 <= 182:
        s[i] = (1 - 13.0/16) + (1.0/16)/(1+np.exp((t*20 - 178)))
    elif t*20 <= 196:
        s[i] = (1 - 14.0/16) + (1.0/16)/(1+np.exp((t*20 - 192)))
    elif t*20 <= 210:
        s[i] = (1 - 15.0/16) + (1.0/16)/(1+np.exp((t*20 - 206)))
    else:
        s[i] = (1.0/16)/(1+np.exp((t*20 - 220)))

##s the ratio ## down-to-up switching
gon  = 1.0
goff = 160.0
gmem = (1-s)*gon + s*goff  #gon*goff/(s*(gon-goff)+goff) 

m = stair_memristor(0.025, time)

for i,t in enumerate(time):
    if i >= 0:
        m.q_t_pw(i,t)

plt.figure()
plt.plot(time*20, gmem, label = 'staircase')
#plt.plot(time*20, m.g, '--', label = 'ideal staircase')
plt.xlabel(r'$k_p\varphi$', fontsize = 16)
plt.ylabel(r'$g(k_p\varphi)$', fontsize = 16)
#plt.xlim([0,70])
plt.legend(loc=4,ncol=1)
    
plt.figure()
plt.subplot(211)
plt.plot(time*20,s)
plt.grid(True)
#plt.xlim([0,10])
plt.subplot(212)
plt.plot(time, ds)
plt.grid(True)
plt.show()
