import numpy as np 
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

  A = 1       #threshold
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
    self.phi[t] = 2.0*q + (q**3)/4.0
    
## calculate flux when input is ##square wave##
## piecewise linear memristor
## @parameter t index
  def phi_t_pw(self, t):
    A = 6
    r_on = 10
    r_off = 100
    """ cal phi(t) from q """
    q = self.q[t]
    if q > A:
      self.phi[t] = r_off*q + (r_on-r_off)*A
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
    self.r[t] = 3.0*(self.q[t]**2)/4.0 + 2.0
    
## keep previous value
  def keepPre(self, qvalue, phivalue, rvalue, index):
    self.q[index]   = qvalue
    self.phi[index] = phivalue
    self.r[index]   = rvalue

######################################################
##########       flux control memristor       ########
######################################################
    
class memristor_flux:
  def __init__(self, dt, time):
    self.g   = np.ones(len(time))  ##matrix of ones
    self.v   = np.zeros(len(time))
    self.i   = np.zeros(len(time))
    self.phi = np.zeros(len(time)) 
    self.q   = np.zeros(len(time))
    self.dt  = dt

## calculate phi from integral of voltage
  def calPhi(self, t, voltage):
    self.v[t] = voltage
    if t > 0:
      ##self.phi[t] = self.phi[t-1] + self.dt * self.v[t] ##integral of voltage
      self.phi[t] = (self.v[t-1] + self.v[t])*self.dt/2 + self.phi[t-1]

## calculate charge from phi
  def calCharge_cubic(self, t):
    phi = self.phi[t]
    self.q[t] = phi**(1.0/1.5)

## calculate Mem from phi
  def calMem(self, t):
    phi = self.phi[t]
    self.g[t] = (1.0/1.5)*(phi**(1.0/1.5 - 1))

## keep the pevious value
  def keepPre(self, qvalue, phivalue, gvalue, index):
    self.q[index]   = qvalue
    self.phi[index] = phivalue
    self.g[index]   = rvalue

## piecewise linear memristor
  def memPw(self, t):
    A = 6
    r_on = 10
    r_off = 100
    """ cal phi(t) from q """
    phi = self.phi[t]
    if phi > A:
      self.q[t] = r_off*phi + (r_on-r_off)*A
    else:
      self.q[t] = r_on*phi
  
