import numpy as np
import pylab as plt
import cmemristor as cm
import spike_generator as sp
import LifNeuron as lif
import StdpTraing as st
import random as ran
import os.path

######this file generate default post spike time and default positive update trace######
######it reads a default pre spike time and default memristor setting#####

########set the path############
rpath = 'C:/Users/xy24/Google Drive/code/\
Memristor Simulation/trace/net - Copy/dataset/'

prespike_time_path = os.path.join(rpath,'default_pre_spike_time')
postspike_time_path = os.path.join(rpath,'default_postspike_time')
postspike_trace_path = os.path.join(rpath,'default_postspike_trace')

positive_update_trace_path = os.path.join(rpath,'default_positive_update_trace')


##simulation parameters
dt   = 0.5 ##0.025    improve speed
time = np.arange(0,400+dt,dt)

##Create a presynaptic spike generator 
genSpike   = sp.TraceGenerator(dt,time)
channelNum = 10

##read the pre time spike train
f = open(prespike_time_path,'r')
pre_time = []

for line in f:
    tmp = [int(item) for item in line.split()]
    pre_time.append(tmp)
f.close()

## generate pre spike train
train = []

for i in range(10):
    train.append(genSpike.getTrace(pre_time[i],1))


def sumTrain():
    total_train = np.zeros(len(time))
    for i in range(len(train)):
        total_train += train[i]
    return total_train

summedTrain = sumTrain()
        
###############################
# create memristors and set them
###############################
mem0 = cm.memristor_flux(dt,time)
mem0.phi[0] = 0.2
mem0.calCharge_cubic(0)
mem0.calMem(0)

mem1 = cm.memristor_flux(dt,time)
mem1.phi[0] = 0.7
mem1.calCharge_cubic(0)
mem1.calMem(0)

mem2 = cm.memristor_flux(dt,time)
mem2.phi[0] = 0.5
mem2.calCharge_cubic(0)
mem2.calMem(0)

mem3 = cm.memristor_flux(dt,time)
mem3.phi[0] = 0.4
mem3.calCharge_cubic(0)
mem3.calMem(0)

mem4 = cm.memristor_flux(dt,time)
mem4.phi[0] = 0.3
mem4.calCharge_cubic(0)
mem4.calMem(0)

mem5 = cm.memristor_flux(dt,time)
mem5.phi[0] = 0.25
mem5.calCharge_cubic(0)
mem5.calMem(0)

mem6 = cm.memristor_flux(dt,time)
mem6.phi[0] = 0.35
mem6.calCharge_cubic(0)
mem6.calMem(0)

mem7 = cm.memristor_flux(dt,time)
mem7.phi[0] = 0.3
mem7.calCharge_cubic(0)
mem7.calMem(0)

mem8 = cm.memristor_flux(dt,time)
mem8.phi[0] = 0.1
mem8.calCharge_cubic(0)
mem8.calMem(0)

mem9 = cm.memristor_flux(dt,time)
mem9.phi[0] = 0.6
mem9.calCharge_cubic(0)
mem9.calMem(0)

print(mem0.g[0])
print(mem1.g[0])
print(mem2.g[0])
print(mem3.g[0])
print(mem4.g[0])
print(mem5.g[0])
print(mem6.g[0])
print(mem7.g[0])
print(mem8.g[0])
print(mem9.g[0])

## create a LIF neuron
for t in range(1):
    x = train[0]*mem0.g[t] + train[1]*mem1.g[t] + train[2]*mem2.g[t] + train[3]*mem3.g[t]\
        + train[4]*mem4.g[t] + train[5]*mem5.g[t] + train[6]*mem6.g[t] + train[7]*mem7.g[t]\
        + train[8]*mem8.g[t] + train[9]*mem9.g[t]
    lif      = lif.LifNeuron(dt,time)
    lifOut   = lif.getLifOut(x)   ##get output of LIF
post_time = lif.sptime
btrain   = genSpike.getTrace(post_time,-1)
print post_time

#####save post spike time in file
##file_postspike_time = open(postspike_time_path,'a')
##file_postspike_time.write(str(post_time)+'\n')
##f.close

#####save post spike trace in file
post_spike_trace = genSpike.getTrace(post_time,-1)
np.savetxt(postspike_trace_path, post_spike_trace, \
           fmt = '%1.4e',delimiter = ',')

## get the learning area for specific channel
stdp = st.StdpTraining(dt,time, genSpike)

#generate positive update trace and save it in file
positive_trace = np.zeros((len(pre_time),len(time)))
for i in range(len(pre_time)):
    positive_trace[i] = stdp.updateTracePre(pre_time[i], post_time)

np.savetxt(positive_update_trace_path, positive_trace, \
               fmt = '%1.4e',delimiter =',')


plt.figure()
plt.plot(time,positive_trace[2],'b')
plt.plot(pre_time[2],[0.1]*len(pre_time[2]),'b*')
plt.plot(post_time,  [0.1]*len(post_time),  'ro')
plt.show()
