from __future__ import division
from cmemristor import memristor
from numpy import *
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

pthreshold = 106
nthreshold = -106

TE    = 58
etime = arange(55+dt+dt,TE+dt,dt)
newtime = append(time,etime)
ling = zeros(len(etime))

## HH Parameters
V_rest  = 0      # mV
Cm      = 1      # uF/cm2
gbar_Na = 120    # mS/cm2
gbar_K  = 36     # mS/cm2
gbar_l  = 0.3    # mS/cm2
E_Na    = 115    # mV
E_K     = -12    # mV
E_l     = 10.613 # mV

Vm      = zeros(len(time)) # mV
Vm[0]   = V_rest
m       = m_inf(V_rest)      
h       = h_inf(V_rest)
n       = n_inf(V_rest)

Vmax = Vm[0]

## Stimulus
I = zeros(len(time))
for i, t in enumerate(time):
  if 10 <= t <= 15: I[i] = 10 # uA/cm2

## Simulate Model
for i in range(1,len(time)):
  g_Na = gbar_Na*(m**3)*h
  g_K  = gbar_K*(n**4)
  g_l  = gbar_l

  m += dt*(alpha_m(Vm[i-1])*(1 - m) - beta_m(Vm[i-1])*m)
  h += dt*(alpha_h(Vm[i-1])*(1 - h) - beta_h(Vm[i-1])*h)
  n += dt*(alpha_n(Vm[i-1])*(1 - n) - beta_n(Vm[i-1])*n)

  Vm[i] = Vm[i-1] + (I[i-1] - g_Na*(Vm[i-1] - E_Na) - g_K*(Vm[i-1] - E_K) - g_l*(Vm[i-1] - E_l)) / Cm * dt
  
  if Vm[i] > Vmax:
    Vmax = Vm[i]

print Vmax

##add zero to Vm get 2 arrays
Vm1 = append(Vm,ling)
Vm2 = append(ling,Vm)

Vmem = Vm1 - Vm2

mmm  = memristor(dt, newtime)
Im  = zeros(len(newtime))
Vdiff = zeros(len(newtime))
phi = zeros(len(newtime))

## Set up emristor ##
mmm.q[0] = 8
mmm.phi_t_cubic_poly(0)
mmm.r_t(0)
print(mmm.r[0])

for i, t in enumerate(newtime):
  if Vmem[i] > pthreshold or Vmem[i] < nthreshold:
    Im[i] = Vmem[i]/mmm.r[i-1]
    mmm.q_t(i, Im[i])
    if mmm.q[i] < 0:
     mmm.q[i] = 0
    mmm.phi_t_cubic_poly(i)
    mmm.r_t(i)
    mmm.v_t(i)
    phi[i] = phi[i-1] + dt*Vmem[i]
  else:
    if i > 0:
     mmm.keepPre(mmm.q[i-1],mmm.phi[i-1],mmm.r[i-1],i)
     phi[i] = phi[i-1]

md =  mmm.r[0] - mmm.r[len(newtime)-1]
print md



figure()
plot(newtime, mmm.q, color= 'r')
plot(newtime, mmm.i)
grid(True)
title('q-t')
ylabel('q')
xlabel('Time (msec)')

figure()
plot(newtime, Vmem, color = 'r')
plot(newtime, mmm.phi)
plot(newtime, phi, color = 'black')
##plot(newtime, Vm1, color='b')
##plot(newtime, Vm2, color='b')
grid(True)
title('Vdiff')
ylabel('Membrane Potential (mV)')
xlabel('Time (msec)')

####plot membrane potential trace
##figure()
##plot(time, Vm, time, -30+I)
##title('Hodgkin-Huxley Example')
##ylabel('Membrane Potential (mV)')
##xlabel('Time (msec)')

show()
