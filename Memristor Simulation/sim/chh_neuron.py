from __future__ import division
import neuronset as ne
from numpy import *
from pylab import *

class neuron:

  #setup parameters and state variables
  def __init__(self,T,dt,time):
    self.T       = T              #ms total time
    self.dt      = dt             #ms step size
    self.time    = time           #time = np.arange(0, T+dt, dt)
    self.Vm      = zeros(len(time))
    self.m = ne.m
    self.h = ne.h
    self.n = ne.n

  def getOutput(self,i,I):
    time = self.time
    dt   = self.dt                  #step size
       
    self.Vm[0]   = ne.V_rest
    
    if i > 0:
      g_Na = ne.gbar_Na*(self.m**3)*self.h
      g_K  = ne.gbar_K*(self.n**4)
      g_l  = ne.gbar_l
      
      self.m += dt*(ne.alpha_m(self.Vm[i-1])*(1 - self.m) - ne.beta_m(self.Vm[i-1])*self.m)
      self.h += dt*(ne.alpha_h(self.Vm[i-1])*(1 - self.h) - ne.beta_h(self.Vm[i-1])*self.h)
      self.n += dt*(ne.alpha_n(self.Vm[i-1])*(1 - self.n) - ne.beta_n(self.Vm[i-1])*self.n)
      #print(i)
      #print(I)
      self.Vm[i] = self.Vm[i-1] + (I - g_Na*(self.Vm[i-1] - ne.E_Na) - g_K*(self.Vm[i-1] - ne.E_K) - g_l*(self.Vm[i-1] - ne.E_l)) / ne.Cm * dt
      #print(self.Vm[i])
      return self.Vm[i]
    else:
      return self.Vm[0]
