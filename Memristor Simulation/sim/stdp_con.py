import numpy as np
import pylab as plt

class controller:
    def __init__(self,time):
        self.time  = time                  ##simulation time
        self.vdiff = np.zeros(len(time))   ##voltage difference of pre and post neuron outputs
        

    def cal_voltage(self,vneuron1,vneuron2,t):
        threshold = 1                      ##threshold to change memristance
        v1 = vneuron1                      ##pre-neuron output
        v2 = vneuron2                      ##post-neuron output
        self.vdiff[t] = v2 - v1            ##voltage difference
        if self.vdiff[t] > threshold or self.vdiff[t] < - threshold :
            return self.vdiff[t]
            ##Im = self.vdiff/memristor[t-1]
            #memeristor[Im]
            
        
        
