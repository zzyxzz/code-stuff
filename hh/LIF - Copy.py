import numpy as np
import pylab as plt

class lifneuron:
    def __init__(self, dt, time):
        self.Vm = np.zeros(len(time))
        self.sp_time = np.zeros(len(time))
        self.dt = dt

########################    
#set parameters
########################
    t_rest = 0    #initial refractory time
    Rm = 1        #R
    Cm = 10       #C
    tm = Rm*Cm    #time constant
    #t_ref = 16    #refractory period
    Vthr = 1      #spike threshold
    V_spike = 0.5

####stimulus
    #I =1.3
##iterate over time step
    def spike(self,I,t_ref):
        for i, t in enumerate (time):
            if t>t_rest:
                Vm[i]=Vm[i-1]+(-Vm[i-1]+I*Rm)*dt/tm
                if Vm[i]>Vthr:
                    sp_time[i] = 1
                    Vm[i]+=V_spike
                    t_rest = t+t_ref
