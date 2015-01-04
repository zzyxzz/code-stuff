from cmemristor import memristor
from chh_neuron import neuron
#from trans import trans
import numpy as np
import pylab as plt

    
T       = 55               #ms
dt      = 0.025            #ms
time    = np.arange(0,T+dt,dt)
nnn = neuron(T,dt,time)
Vmem = np.zeros(len(time))

## Stimulus of neuron
I = np.zeros(len(time))
for i, t in enumerate(time):
 if 20 <= t <= 24:
     I[i] = 2 # uA/cm2   ###if I<3, no AP ## default value I =10
 if i > 0:
     Vmem[i] = nnn.getOutput(i, I[i-1])
 elif i == 0:
     Vmem[i] = nnn.getOutput(i, I[i])

plt.figure()
plt.plot(time, Vmem)
plt.ylim([-5,20])
#plt.xlim([10,20])
plt.title('Hodgkin-Huxley Neuron')
plt.ylabel('Membrane Potential (mV)')
plt.xlabel('Time (msec)')

plt.plot(time,I)




## Stimulus of memristor
m = memristor(dt, time)
Im = np.zeros(len(time))
##set memristor initial value
m.q[0] = 0
m.phi_t_cubic_poly(0)
m.v_t(0)
m.r_t(0)

for i, t in enumerate(time):
  A = 1
  Im[i] = A*np.sin(t)
  
for i,t in enumerate(time):
    if i > 0:
        m.q_t(i,Im[i])
        m.phi_t_pw(i)
        #m.phi_t_cubic_poly(i)
        m.v_t(i)
        m.r_t(i)
        
plt.figure()
plt.scatter(m.q,m.r,s=0.5)
plt.ylabel('Flux-phi')
plt.xlabel('R')
plt.title('phi-q')

plt.figure()
plt.scatter(m.v,m.i,s=0.5)
plt.ylabel('Current')
plt.xlabel('Voltage')
plt.title('V-I')

#plt.figure()
#plt.scatter(time,m.r,s=0.5)
##plt.scatter(time,Im)
#plt.title('Mrmtistance')

plt.show()
