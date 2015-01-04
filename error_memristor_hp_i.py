import numpy as np 
from scipy.signal.waveforms import square 
import pylab as plt

################################################################################
# current controled HP memristor 
################################################################################
class memristor:
  def __init__(self, sim_t, dt):#=0.25):
    self.ts = t = np.arange(0, sim_t+dt, dt)
    self.n = len(t)
    self.r = np.zeros(len(t))
    self.v = np.zeros(len(t))
    self.i = np.zeros(len(t))
    self.phi = np.zeros(len(t)) 
    self.q = np.zeros(len(t))
    self.w = np.zeros(len(t))
    self.dt = dt
    self.Ron = 1
    self.Roff = 160
    self.Uv = 5*10e-2 
    self.D = 1.0 

	
  def q_i_t(self, t):
    """ cal q(t) from i """
    if t > 0:
      self.q[t] = self.q[t-1] + self.dt*self.i[t]

  def phi_v_t(self, t):   
    """ cal phi(t) from v """
    if t > 0:
      self.phi[t] = self.phi[t-1] + self.dt*self.v[t]

  def w_q_t(self, t):   
    """ cal w(t) from q """
    self.w[t] = self.Uv * self.Ron * self.q[t] / self.D
    if self.w[t] < 0:
      self.w[t] = 0;
    if self.w[t] > self.D:
      self.w[t] = self.D

  def r_q_t(self, t):
    """ cal R = Roff * (1 - Uv*Ron*q/(D**2)) """
    self.r[t] = self.Roff * (1 - self.Uv*self.Ron*self.q[t]/(self.D**2)) 
 
  def v_r_t(self, t):
    """ cal v(t) = R(t)*i(t) """
    self.v[t] = self.r[t] * self.i[t]
 
##
##if __name__ == "__main__":
##################################################################################
### input (charge controled memristor)
##################################################################################
##
#### (A) sinusoidal current sourse
##  m = memristor(sim_t=6.0*np.pi, dt=0.025)
##  for i, t in enumerate(m.ts):
##    A = 0.01 
##    m.i[i] = A*np.sin(t)
####  m.i[i] = A*np.sin(t-np.pi*0.5) + 1.0
##
##"""
## (B) square wave

#ds = np.arange(1, 20+0.1, 0.1)
ds = np.arange(1.0,10.0+1.0, 1.0)
error = []
last = 0.0

for t in ds:
  m = memristor(sim_t=10.0*np.pi, dt=0.025)
  m.i = 0.05*(1.0*square(t*m.ts, duty=0.5)+1.0) 
  
  for i,term in enumerate(m.ts):
    m.q_i_t(i)
    m.w_q_t(i)
    m.r_q_t(i)
    if m.r[i] <= 350.0 and m.i[i]==0.0:
      #print m.r[i]
      error.append(abs(300.0-m.r[i]))
      break
#print error
##plt.figure()
##plt.plot(m.ts, m.i)
print error
print sum(np.array(error)**2)/10

plt.figure()
plt.bar(ds, error,width = 0.5)
    
##plt.subplot(2,2,1)
##plt.plot(m.q, m.phi)
##
##plt.subplot(2,2,2)
##plt.plot(m.i, m.v)
##
##plt.subplot(2,2,3)
##plt.plot(m.ts, m.i)
###plt.plot(m.ts, m.i, m.ts, m.q, m.ts, m.v)
##
##plt.subplot(2,2,4)
##plt.plot(m.ts, m.w)
###plt.plot(m.ts, m.v, m.ts, m.phi, m.ts, m.r)
##
plt.show()
