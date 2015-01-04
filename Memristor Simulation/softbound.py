from soft_bound_memristor import memristor
import numpy as np
import pylab as plt

T       = 55               #ms
dt      = 0.025            #ms
time    = np.arange(0,T+dt,dt)

## Stimulus of memristor
m = memristor(dt, time)
Im = np.zeros(len(time))
yj = np.zeros(len(time))
##set memristor initial value
m.q[0] = 0
m.phi_t_cubic_poly(0)
m.v_t(0)
m.r_t(0)

A = 3
Im = A*np.sin(time)
  
for i,t in enumerate(Im):
    if i > 0:
        m.q_t(i,t)
        m.phi_t_pw(i)
        #m.phi_t_cubic_poly(i)
        m.v_t(i)
        m.r_t(i)

r = 1-(2*m.q/100 - 1)**2
y = 3*r
for i,t in enumerate(time):
    if i > 0:
        yj[i] = (y[i-1] + y[i])*dt/2 + yj[i-1]

plt.figure()
plt.scatter(m.q,yj,s=0.5)
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
