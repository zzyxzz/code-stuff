from cmemristor_gai import stair_memristor
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
    #s[i] =  1/(1+np.exp(t*12 - 10))
    #ds[i] = -4 * np.exp(t*4 - 10)/((1 + np.exp(t*4 - 10))**2)
    if t*20 <= 14:
        s[i] = (1 - 1.0/4)  + (1.0/4)/(1+np.exp(t*20 -10))
    elif t*20 <= 28:
        s[i] = (1 - 2.0/4) + (1.0/4)/(1+np.exp((t*20 - 24)))
    elif t*20 <= 42:
        s[i] = (1 - 3.0/4) + (1.0/4)/(1+np.exp((t*20 - 38)))
    else:
        s[i] = (1.0/4)/(1+np.exp((t*20 - 52)))

##s the ratio ## down-to-up switching
gon  = 4
goff = 0.01
gmem = (1-s)*gon + s*goff

m = stair_memristor(0.025, time)

for i,t in enumerate(time):
    if i >= 0:
        m.q_t_pw(i,t)

plt.figure()
plt.plot(time*20, gmem, label = 'staircase')
plt.plot(time*20, m.g, '--', label = 'ideal staircase')
plt.xlabel(r'$k_p\varphi$', fontsize = 16)
plt.ylabel(r'$g(k_p\varphi)$', fontsize = 16)
plt.xlim([0,70])
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
