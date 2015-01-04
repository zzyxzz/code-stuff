import numpy as np
import pylab as plt

################
#mem class
################

class memristor:
    def __init__(self, dt, time):
        #self.r = np.zeros(len(time))
        #self.v = np.zeros(len(time))
        #self.i = np.zeros(len(time))
        self.g = np.ones(len(time))
        self.phi = np.zeros(len(time))
        self.s = np.zeros(len(time))
        self.dt = dt
        self.time = time
        self.gon = 7
        self.goff = 2
        self.kp = 1
        self.k = 7
        for i,t in enumerate(time):
            self.g[i] = 2
        

    def cal_g(self, v, i):
        if i > 0:
            self.phi[i] = self.phi[i-1] + self.dt*v
            self.s[i] = 1/(1+np.exp(-self.phi[i]*self.kp + self.k))
            self.g[i] = (1-self.s[i])*self.goff + self.s[i]*self.gon

    def keep_pre(self, i):
        self.phi[i] = self.phi[i-1]
        self.s[i] = self.s[i-1]
        self.g[i] = self.g[i-1]
        
if __name__ == '__main__':
    data = np.arange(0, 6, 0.05)
    in_sin = 20*np.sin(np.pi*data)
    mem = memristor(0.05, in_sin)
    for i,t in enumerate(in_sin):
        mem.cal_g(t,i)
    
    plt.figure()
    plt.plot(in_sin*mem.g,in_sin)
    plt.figure()
    plt.plot(data,mem.s)
    plt.show()
