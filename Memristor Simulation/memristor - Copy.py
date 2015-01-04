import numpy as np 
from scipy.signal.waveforms import square 
import pylab as plt

################################################################################
# memristor 
################################################################################
class memristor:
  def __init__(self, sim_t, dt):
    self.ts = t = np.arange(0, sim_t+dt, dt) ##0.25=dt
    self.n = len(t)
    self.r = np.zeros(len(t))
    self.v = np.zeros(len(t))
    self.i = np.zeros(len(t))
    self.phi = np.zeros(len(t)) 
    self.q = np.zeros(len(t))
    self.dt = dt
##########################
# Parameters
##########################

  B = 1
  r_on = 10   #minimum value of memristance
  r_off = 100 #maximum value of memristance

##########################
# Methods
##########################

## calculate charge
## @parameter t index
  def q_t(self, t):            
    """ cal q(t) from i """
    if t > 0:
      self.q[t] = self.q[t-1] + self.dt*self.i[t]   #q = integral of i
       
## calculate flux
## @parameter t index
  def phi_t_cubic_poly(self, t):   
    """ cal phi(t) from q """
    q = self.q[t]
    if q < 1.0:
      self.phi[t] = q + (q**3)/4.0
    else:
      self.phi[t] = q**2 + 0.25
    """think about another function link first one well"""  
    
## calculate flux when input is square wave
## @parameter t index
  def phi_t_pw(self, t):   
    """ cal phi(t) from q """
    q = self.q[t]
    if (q < -B):
      self.phi[t] = r_off*q + (r_off-r_on)*B
    elif (q > B):
      self.phi[t] = r_off*q + (r_on-r_off)*B
    else:
      self.phi[t] = r_on*q

## caculate voltage
## @parameter t index
  def v_t(self, t):
    """ cal v(t) = dphi/dt """
    if t == 0:
      self.v[t] = (self.phi[t] - 0.0)/self.dt
    else:
      self.v[t] = (self.phi[t] - self.phi[t-1])/self.dt

## calculate memristance
## @parameter t index
  def r_t(self, t):
    """ cal r(t) = dphi/dq """
    if t == 0:
      self.r[t] = 1.0
    else:
      if self.q[t] == self.q[t-1]:
        self.r[t] = self.r[t-1]
      else:
        self.r[t] = (self.phi[t] - self.phi[t-1])/(self.q[t]-self.q[t-1])
 

################################################################################
# input (charge controled memristor)
################################################################################

## (A) sinusoidal current sourse 
m = memristor(sim_t=4.2*np.pi, dt=0.25)
for i, t in enumerate(m.ts):
  A = 0.8
  m.i[i] = A*np.sin(0.5*t)
##  m.i[i] = A*np.sin(t-np.pi*0.5) + 1.0

"""
## (B) square wave 
m = memristor(sim_t=100.0*np.pi, dt=0.025)
m.i = 0.025*(1.0*square(1.0*m.ts, duty=0.09)+1.0) 
"""

################################################################################
# Simulate
################################################################################

for i,t in enumerate(m.ts):
  m.q_t(i)
  m.phi_t_cubic_poly(i)
#  m.phi_t_pw(i)
  m.v_t(i)
  m.r_t(i)

##txt = open("wrtie_it.txt", "w")
##for item in m.q:
##  tt = str(item)
##  txt.writelines("%s\n" %tt)
##txt.close()

plt.figure()
plt.subplot(2,2,1)
plt.scatter(m.q, m.phi,s=0.5)
plt.ylabel('Flux-phi')
plt.xlabel('Charge-q')

plt.subplot(2,2,2)
plt.scatter(m.i, m.v,s=0.5)
plt.ylabel('Voltage-v')
plt.xlabel('Current-i')

plt.subplot(2,2,3)
plt.plot(m.ts, m.i, m.ts, m.q)
plt.ylabel('Current-i;Charge-q')
plt.xlabel('Time')

plt.subplot(2,2,4)
plt.plot(m.ts, m.r)
#plt.plot(m.ts, m.v, m.ts, m.phi, m.ts, m.r)
plt.ylabel('Memristance-M')
plt.xlabel('Time')
plt.show()
