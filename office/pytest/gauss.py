import random
import numpy as np
import pylab as plt
import LifNeuron as lif
import bounded_memristor as bm
import spike_generator as sp

#y=np.random.normal(0,0.5,1000)
#plt.hist(y,bins=50,normed=True)

##simulation parameters
dt   = 0.025
time = np.arange(0,400+dt,dt)

##Create a presynaptic spike generator 
genSpike   = sp.TraceGenerator(dt,time)

pre_time = []

##read the pre time spike train
f = open('pre','r')
for line in f:
    tmp = [float(item) for item in line.split()]
    pre_time.append(tmp)
f.close()

## generate pre spike train
train = []

for ch in range(10):
    train.append(genSpike.getTrace(pre_time[ch],1))

mem = []
init_phi = [0.2, 0.7, 0.5, 0.4, 0.3, 0.25, 0.35, 0.3, 0.1, 0.6] #[0.7, 0.5, 0.4, 0.3, 0.25, 0.35, 0.3, 0.1, 0.6, 0.2]

for ch in range(len(train)):
    mem.append(bm.memristor_flux(dt,time))
    mem[ch].phi[0] = init_phi[ch]
    mem[ch].calCharge_cubic(0)
    mem[ch].calMem(0)

def sumTrain():
    total_train = np.zeros(len(time))
    for ch in range(len(train)):
        total_train += train[ch]*mem[ch].g[0]
        print mem[ch].g[0]
    return total_train

lif      = lif.LifNeuron(dt,time)

for i in range(2):
    pre_spike = sumTrain()
    lifOut   = lif.getLifOut(pre_spike) ##get real output of LIF
    postTime = lif.sptime             ##get real post spike time train
    print postTime
    plt.figure()
    plt.plot(time,lifOut)
    plt.figure()
    plt.plot(time,pre_spike)

plt.show()
