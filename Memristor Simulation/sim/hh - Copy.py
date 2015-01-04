from __future__ import division
from cmemristor import memristor
from numpy import *
from pylab import *

## setup parameters and state variables
T     = 90    # ms
dt    = 0.025 # ms
time  = arange(0,T+dt,dt)#time  = arange(0,T+dt,dt)

mmm  = memristor(dt, time)

## Set up emristor ##
mmm.q[0] = 8
mmm.phi_t_cubic_poly(0)
mmm.r_t(0)
print(mmm.r[0])

for i, t in enumerate(time):
  mmm.q_t(i, 0.5)
  if mmm.q[i] < 0:
    mmm.q[i] = 0
  mmm.phi_t_cubic_poly(i)
  mmm.r_t(i)
  mmm.v_t(i)

figure()
plot(mmm.q, mmm.phi, color= 'r')
grid(True)
title('q-t')
ylabel('q')
xlabel('Time (msec)')

figure()
plot(time, mmm.r, color = 'r')
grid(True)


show()
