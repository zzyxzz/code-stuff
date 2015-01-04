import numpy as np

class trans:

    def __init__(self, time):
        self.v = np.zeros(len(time))
        
    def getTranOut(self, Vi):
        n = Vi
        a = 1/(1+np.exp(-n))
        return a
