from numpy import *
from pylab import *

#set parameter

R = 1
C = 10
I_in = 2 # input current

T = 50 #simulation time 50s
dt = 0.125 # time step
t = arange(0,T+dt,dt)
t_t = R*C

V = zeros(len(t))
Vth = 1  #threshold
V_spike = 0.5
t_ref = 0 #initial refractory time
t_refp = 4


for i, tt in enumerate(t):
   if tt >= t_ref:
      V[i] = V[i-1] + dt/t_t*(I_in*R - V[i-1])
      if V[i] >= Vth:
         V[i] = V[i] + V_spike
         t_ref = tt + t_refp

#plot
plot(t,V)
title('LIF')
xlabel('time')
ylabel('voltage')
ylim([0,2])
show()
