import numpy as np 
from scipy.signal.waveforms import square 
import pylab as plt

################################################################################
# memristor 
################################################################################
class memristor:
  def __init__(self, dt, time):
    self.r = np.ones(len(time))  ##matrix of ones
    self.v = np.zeros(len(time))
    self.i = np.zeros(len(time))
    self.phi = np.zeros(len(time)) 
    self.q = np.zeros(len(time))
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
  def q_t(self, t, I):
    """ cal q(t) from i """
    self.i[t] = I
    if t > 0:
      self.q[t] = self.q[t-1] + self.dt*self.i[t]   #q = integral of i
       
## calculate flux
## @parameter t index
  def phi_t_cubic_poly(self, t):   
    """ cal phi(t) from q """
    q = self.q[t]
    ##if q < 1.0:
    ##  self.phi[t] = q + (q**3)/4.0
    ##else:
    ##  self.phi[t] = q**2 + 0.25
    """think about another function link first one well"""
    self.phi[t] = q + (q**3)/4.0
    
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
      self.r[t] = 2
    else:
      if self.q[t] == self.q[t-1]:
        self.r[t] = self.r[t-1]
      else:
        self.r[t] = (self.phi[t] - self.phi[t-1])/(self.q[t]-self.q[t-1])

  def rChange(self,value,index):
    self.r[index] = value

##"""
#### (B) square wave 
##m = memristor(sim_t=100.0*np.pi, dt=0.025)
##m.i = 0.025*(1.0*square(1.0*m.ts, duty=0.09)+1.0) 
##"""
