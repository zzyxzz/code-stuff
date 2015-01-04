import numpy as np 
from scipy.signal.waveforms import square 
import pylab as plt

################################################################################
# current controled HP memristor 
################################################################################
class memristor:
  def __init__(self, sim_t, dt=0.25):
    self.ts = t = np.arange(0, sim_t+dt, dt)
    self.n = len(t)
    self.r = np.zeros(len(t))
    self.v = np.zeros(len(t))
    self.i = np.zeros(len(t))
    self.phi = np.zeros(len(t)) 
    self.q = np.zeros(len(t))
    self.w = np.zeros(len(t))
    self.dt = dt
    self.Ron = 100
    self.Roff = 16000
    self.Uv = 100 
    self.D = 1

	
  def q_i_t(self, t):
    """ cal q(t) from i """
    if t > 0:
      self.q[t] = self.q[t-1] + self.dt*self.i[t]

  def phi_v_t(self, t):   
    """ cal phi(t) from v """
    if t == 0:
      self.phi[t] = 0 + self.dt*self.v[t]
    elif self.w[t-1] == self.D and self.v[t] > 0 and self.v[t-1] > 0:
      self.phi[t] = self.phi[t-1] 
    elif self.w[t-1] == 0 and self.v[t] < 0 and self.v[t-1] < 0:
      self.phi[t] = self.phi[t-1] 
    else: 
      self.phi[t] = self.phi[t-1] + self.dt*self.v[t]

  def q_phi_t(self, t):
    """ cal q from phi """
    a = self.Uv * self.Ron * self.Roff/(2.0 * (self.D**2))
    b = self.Roff
    c = self.phi[t]

    d = (0.25*(b**2)/a - c)/a
    if d < 0:
      d = 0
    e = np.sqrt(d)
    self.q[t] = 0.5*b/a - e

  def w_q_t(self, t):   
    """ cal w(t) from q """
    self.w[t] = self.Uv * self.Ron * self.q[t] / self.D
    if self.w[t] < 0:
      self.w[t] = 0
    if self.w[t] > self.D:
      self.w[t] = self.D

  def r_q_t(self, t):
    """ cal R = Roff * (1 - Uv*Ron*q/(D**2)) """
    self.r[t] = self.Roff * (1 - self.Uv*self.Ron*self.q[t]/(self.D**2)) 
    if self.r[t] > self.Roff:
      self.r[t] = self.Roff
    if self.r[t] < self.Ron:
      self.r[t] = self.Ron
 
  def i_r_t(self, t):
    """ cal v(t) = R(t)*i(t) """
    self.i[t] = self.v[t] / self.r[t]
 


################################################################################
# input (charge controled memristor)
################################################################################

## (A) sinusoidal current sourse

t0 = 2.0 
m = memristor(sim_t=6.0/t0, dt=0.001)
for i, t in enumerate(m.ts):
  A = 2
  m.v[i] = A*np.sin(t0*np.pi*t)


##t0 = 2.0
##m = memristor(sim_t=6.0/t0, dt=0.001)
##for i, t in enumerate(m.ts):
##  A = 1.0 
##  if t < (6.0/t0)/2.0:
##      m.v[i] = A*np.sin(t0*np.pi*t)*np.sin(t0*np.pi*t)
##  else:
##      m.v[i] = -A*np.sin(t0*np.pi*t)*np.sin(t0*np.pi*t)

"""
## (B) square wave 
m = memristor(sim_t=100.0*np.pi, dt=0.025)
m.v = 0.025*(1.0*square(1.0*m.ts, duty=0.09)+1.0) 
"""


################################################################################
# Simulate
################################################################################
for i,t in enumerate(m.ts):
  m.phi_v_t(i)
  m.q_phi_t(i)
  m.w_q_t(i)
  m.r_q_t(i)
  m.i_r_t(i)

m2 = memristor(sim_t=6.0/t0, dt=0.001)
for i, t in enumerate(m2.ts):
  A = 2.0 
  m2.v[i] = A*np.sin(2*t0*np.pi*t)


for i,t in enumerate(m2.ts):
  m2.phi_v_t(i)
  m2.q_phi_t(i)
  m2.w_q_t(i)
  m2.r_q_t(i)
  m2.i_r_t(i)

m3 = memristor(sim_t=6.0/t0, dt=0.001)
for i, t in enumerate(m3.ts):
  A = 2.0 
  m3.v[i] = A*np.sin(10*t0*np.pi*t)

for i,t in enumerate(m3.ts):
  m3.phi_v_t(i)
  m3.q_phi_t(i)
  m3.w_q_t(i)
  m3.r_q_t(i)
  m3.i_r_t(i)
  
plt.figure()
plt.plot(m.v,m.i*1000)
plt.plot(m2.v,m2.i*1000)
plt.plot(m3.v,m3.i*1000)
plt.xlabel('Voltage (V)')
plt.ylabel('Current (mA)')


plt.show()
