import numpy as np

class TraceGenerator:
    def __init__(self,dt,time):
        ##simulation parameters
        self.dt   = dt
        self.time = time
    
    ##trace1
    def trace1(self,det,d):        ##d -- indicate pre spike(1) or post spike(-1)
        ##trace parameters
        if d == 1:                ##pre  spike parameters
            tau = 10
            A   = 0.2             ## amplitude
        if d == -1:               ##post spike parameters
            tau = 10
            A   = 0.2
        tx = np.zeros(len(self.time))
        for i ,t in enumerate(self.time):
            if t >= det:          ##det -- indicate the start time of spike
                tx[i] = A* np.exp((-t+det)/tau)
        return tx

    ##trace2
    def trace2(self,det,d):        ##d -- indicate pre spike(1) or post spike(-1)
        ##trace parameters
        if d == 1:                ##pre  spike parameters
            tau = 10
            A   = 0.2             ## amplitude
        if d == -1:               ##post spike parameters
            tau = 10
            A   = 0.2
        tx = np.zeros(len(self.time))
        for i ,t in enumerate(self.time):
            if t >= det:          ##det -- indicate the start time of spike
                if t <= (det+80):
                    tx[i] = A* np.exp((-t+det)/tau)
                else:
                    tx[i] = 0
        return tx
    
    ####all2all
    def getTrace(self,train,d):   ##d -- indicate pre spike(1) or post spike(-1)
        temp    = np.zeros(len(self.time))
        txtotal = temp
        for t in train:
            temp     = self.trace2(t,d)       ############change trace Mode
            txtotal += temp       ##sum the traces
        return txtotal

    def getTraceNearest(self, train):
        index = 0
        tau = 7
        A = 0.2
        tx = np.zeros(len(self.time))
        
        for i,t in enumerate(self.time):
            if index < (len(train) -1):
                if t < train[0]:
                    tx[i] = 0
                if train[index] < t < train[index+1] :
                    tx[i] = A* np.exp((-t+train[index])/tau)
                if t >= train[index+1]:
                    index = index +1
                    tx[i] = A* np.exp((-t+train[index])/tau)
            else:
                tx[i] = A* np.exp((-t+train[index])/tau)
        return tx
                
            
                
            
