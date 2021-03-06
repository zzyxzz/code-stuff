from __future__ import division
import numpy as np
from pylab import *

## Functions
# K channel
alpha_n = vectorize(lambda v: 0.01*(-v + 10)/(exp((-v + 10)/10) - 1) if v != 10 else 0.1)
beta_n  = lambda v: 0.125*exp(-v/80)
n_inf   = lambda v: alpha_n(v)/(alpha_n(v) + beta_n(v))

# Na channel (activating)
alpha_m = vectorize(lambda v: 0.1*(-v + 25)/(exp((-v + 25)/10) - 1) if v != 25 else 1)
beta_m  = lambda v: 4*exp(-v/18)
m_inf   = lambda v: alpha_m(v)/(alpha_m(v) + beta_m(v))

# Na channel (inactivating)
alpha_h = lambda v: 0.07*exp(-v/20)
beta_h  = lambda v: 1/(exp((-v + 30)/10) + 1)
h_inf   = lambda v: alpha_h(v)/(alpha_h(v) + beta_h(v))

### channel activity ###
#v = arange(-50,151) # mV
#figure()
#plot(v, m_inf(v), v, h_inf(v), v, n_inf(v))
#legend(('m','h','n'))
#title('Steady state values of ion channel gating variables')
#ylabel('Magnitude')
#xlabel('Voltage (mV)')

## setup parameters and state variables
T     = 55    # ms
dt    = 0.025 # ms
time  = arange(0,T+dt,dt)#time  = arange(0,T+dt,dt)
xais = linspace(0,999,1000)

## HH Parameters
V_rest  = 0      # mV
Cm      = 1      # uF/cm2
gbar_Na = 120    # mS/cm2
gbar_K  = 36     # mS/cm2
gbar_l  = 0.3    # mS/cm2
E_Na    = 115    # mV
E_K     = -12    # mV
E_l     = 10.613 # mV

Vm      = np.zeros(len(time)) # mV
Vm[0]   = V_rest
m       = m_inf(V_rest)      
h       = h_inf(V_rest)
n       = n_inf(V_rest)

## Stimulus
I = np.zeros(len(time))
#s = np.random.standard_normal(1000)
s = np.random.normal(0,3,1000)
##s = s*10

for i, t in enumerate(time):
  if i < 1000:
    I[i*2] = s[i] # uA/cm2

## Simulate Model
for i in range(1,len(time)):
  g_Na = gbar_Na*(m**3)*h
  g_K  = gbar_K*(n**4)
  g_l  = gbar_l

  m += dt*(alpha_m(Vm[i-1])*(1 - m) - beta_m(Vm[i-1])*m)
  h += dt*(alpha_h(Vm[i-1])*(1 - h) - beta_h(Vm[i-1])*h)
  n += dt*(alpha_n(Vm[i-1])*(1 - n) - beta_n(Vm[i-1])*n)

  Vm[i] = Vm[i-1] + (I[i-1] - g_Na*(Vm[i-1] - E_Na) - g_K*(Vm[i-1] - E_K) - g_l*(Vm[i-1] - E_l)) / Cm * dt 

####add zero to Vm get 2 arrays
##Vm1 = append(Vm,ling)
##Vm2 = append(ling,Vm)
##
##Vmem = Vm2 - Vm1

figure()
plot(time, Vm)
title('Action Potential')
ylabel('Membrane Potential (mV)')
xlabel('Time (ms)')

figure()
plot(time,I)
title('Stimuli')
ylabel('Input current (mA)')
xlabel('Time (ms)')

figure()
plot(xais,s)

##figure()
##plot(newtime, Vm1, newtime,Vm2 )
##title('Hodgkin-Huxley Example')
##ylabel('Membrane Potential (mV)')
##xlabel('Time (msec)')
  
## plot membrane potential trace
##figure()
##plot(time, Vm, time, -30+I)
##title('Hodgkin-Huxley Example')
##ylabel('Membrane Potential (mV)')
##xlabel('Time (msec)')

show()
