import numpy as np

class LifNeuron:
    def __init__(self,dt,time):
        self.time   = time
        self.dt     = dt
        self.sptime = []         
        ###### LIF parameters
        self.t_rest = 0      ###initial refractory time
        self.Rm          = 1      #R
        self.Cm          = 10     #C
        self.tm          = self.Rm*self.Cm  #time constant
        self.t_ref       = 4      #refractory period
        self.Vthr        = 0.5      #spike threshold
        self.V_spike     = 0.5    #added spike

    def getLifOut(self,datin):
        Vm = np.zeros(len(self.time))
        self.t_rest    = 0
        self.sptime[:] = []
        for i, t in enumerate (self.time):
            if t > self.t_rest:
                Vm[i] = Vm[i-1]+(-Vm[i-1]+datin[i]*self.Rm)*self.dt/self.tm
                if Vm[i] > self.Vthr:
                    self.sptime.append(t)
                    Vm[i]   += self.V_spike
                    self.t_rest = t + self.t_ref
        return Vm
    
