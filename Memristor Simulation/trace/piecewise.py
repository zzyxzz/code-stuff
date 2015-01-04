from cmemristor import memristor
import numpy as np
import pylab as plt

T       = 55               #ms
dt      = 0.025            #ms
time    = np.arange(0,T+dt,dt)

## Stimulus of memristor
m = memristor(dt, time)
Im = np.zeros(len(time))
##set memristor initial value
m.q[0] = 0
m.phi_t_cubic_poly(0)
m.v_t(0)
m.r_t(0)

for i, t in enumerate(time):
  A = 5
  Im[i] = A*np.sin(t)
  
for i,t in enumerate(time):
    if i > 0:
        m.q_t(i,Im[i])
        m.phi_t_pw(i)
        #m.phi_t_cubic_poly(i)
        m.v_t(i)
        m.r_t(i)
        
plt.figure(1)
plt.scatter(m.q, m.phi,s=0.5)
plt.ylabel('Flux-phi')
plt.xlabel('Charge-q')
plt.title('phi-q')
plt.annotate('breakpoint', xy = (6, 60), xytext = (8,60), arrowprops = dict(arrowstyle='->'))
plt.grid(True)

plt.figure(2)
plt.scatter(time,m.i,s=0.5)
plt.ylabel('Current')
plt.xlabel('Voltage')
plt.title('V-I')

#plt.figure()
#plt.scatter(time,m.r,s=0.5)
##plt.scatter(time,Im)
#plt.title('Mrmtistance')

plt.show()
