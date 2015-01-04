import numpy as np

class LifNeuron:
    def __init__(self,dt,time):
        self.time   = time
        self.dt     = dt
        self.sptime = []         
        ###### LIF parameters
        self.t_rest = 0      ###initial refractory time
        self.Rm          = 1.0      #R
        self.Cm          = 10.0     #C
        self.tm          = self.Rm*self.Cm  #time constant
        self.t_ref       = 4.0      #refractory period
        self.Vthr        = 0.5      #spike threshold
        self.V_spike     = 0.5    #added spike
        self.Vm          = np.zeros(len(self.time))

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

    def getLifOutOL(self, datin, i, t):
        if t > self.t_rest:
            self.Vm[i] = self.Vm[i-1]+(-self.Vm[i-1]+datin*self.Rm)*self.dt/self.tm
            if self.Vm[i] > self.Vthr:
                self.sptime.append(t)
                self.Vm[i]   += self.V_spike
                self.t_rest = t + self.t_ref
        return self.Vm[i]
    
