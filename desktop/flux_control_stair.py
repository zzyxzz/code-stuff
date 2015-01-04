import numpy as np
import pylab as plt

################
#mem class
################

class memristor:
    def __init__(self, dt, time):
        #self.r = np.zeros(len(time))
        self.v = np.zeros(len(time))
        #self.i = np.zeros(len(time))
        self.g = np.ones(len(time))
        self.phi = np.zeros(len(time))
        self.s = np.zeros(len(time))
        self.dt = dt
        self.time = time
        self.gon = 7.0
        self.goff = 2.0
        self.kp = 1.0
        self.k = 7.0
        for i,t in enumerate(time):
            self.g[i] = 2.0
        

    def cal_g(self, v, i):
        if i < len(self.time)-1:
            self.g[i] = (1-self.s[i])*self.goff + self.s[i]*self.gon
            self.v[i] = v/self.g[i]
            self.phi[i+1] = self.phi[i] + self.dt*self.v[i]
            self.s[i+1] = 1/(1+np.exp(-self.phi[i+1]*self.kp + self.k))

    def keep_pre(self, i):
        self.phi[i] = self.phi[i-1]
        self.s[i] = self.s[i-1]
        self.g[i] = self.g[i-1]
        
if __name__ == '__main__':
    data = np.arange(0, 2*np.pi/0.96, 0.05)
    in_sin = 40.0*np.sin(data)

    mem = memristor(0.05, data)

    for i,t in enumerate(data):
        mem.cal_g(in_sin[i],i)
    
    plt.figure()
    #plt.plot([1,1],[0,0.5])
    plt.plot(mem.s,1/mem.g)
    plt.show()
