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
Memristor Simulation/trace/net03/dataset/'

class_pre_time_path = os.path.join(rpath,'class_pre_spike_time7')
class_post_time_path = os.path.join(rpath,'actual_class_post_spike_time1')
#postspike_trace_path = os.path.join(rpath,'default_postspike_trace')

#positive_update_trace_path = os.path.join(rpath,'default_positive_update_trace')


##simulation parameters
dt   = 0.5 ##0.025    improve speed
time = np.arange(0,400+dt,dt)

##Create a presynaptic spike generator 
genSpike   = sp.TraceGenerator(dt,time)
channelNum = 10

##read the pre time spike train
f = open(class_pre_time_path,'r')
pre_time = []

for line in f:
    tmp = [int(item) for item in line.split()]
    pre_time.append(tmp)
f.close()
print pre_time

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
mem0.phi[0] = 0.238 #0.197 #0.2 #0.194
mem0.calCharge_cubic(0)
mem0.calMem(0)

mem1 = cm.memristor_flux(dt,time)
mem1.phi[0] = 0.596 #0.642 #0.7 #0.657
mem1.calCharge_cubic(0)
mem1.calMem(0)

mem2 = cm.memristor_flux(dt,time)
mem2.phi[0] = 0.457 #0.467 #0.5 #0.479
mem2.calCharge_cubic(0)
mem2.calMem(0)

mem3 = cm.memristor_flux(dt,time)
mem3.phi[0] = 0.433 #0.457 #0.4 #0.415
mem3.calCharge_cubic(0)
mem3.calMem(0)

mem4 = cm.memristor_flux(dt,time)
mem4.phi[0] = 0.394 #0.357 #0.3 #0.372
mem4.calCharge_cubic(0)
mem4.calMem(0)

mem5 = cm.memristor_flux(dt,time)
mem5.phi[0] = 0.200 #0.243 #0.25 #0.247
mem5.calCharge_cubic(0)
mem5.calMem(0)

mem6 = cm.memristor_flux(dt,time)
mem6.phi[0] = 0.301 #0.274 #0.35 #0.252
mem6.calCharge_cubic(0)
mem6.calMem(0)

mem7 = cm.memristor_flux(dt,time)
mem7.phi[0] = 0.274 #0.324 #0.3 #0.363
mem7.calCharge_cubic(0)
mem7.calMem(0)

mem8 = cm.memristor_flux(dt,time)
mem8.phi[0] = 0.112 #0.096 #0.1 #0.101
mem8.calCharge_cubic(0)
mem8.calMem(0)

mem9 = cm.memristor_flux(dt,time)
mem9.phi[0] = 0.672 #0.685 #0.6 #0.703
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

#save post spike time in file
file_postspike_time = open(class_post_time_path,'a')
file_postspike_time.write(str(post_time)+'\n')
file_postspike_time.close()

#####save post spike trace in file
##post_spike_trace = genSpike.getTrace(post_time,-1)
##np.savetxt(postspike_trace_path, post_spike_trace, \
##           fmt = '%1.4e',delimiter = ',')
##
#### get the learning area for specific channel
##stdp = st.StdpTraining(dt,time, genSpike)
##
###generate positive update trace and save it in file
##positive_trace = np.zeros((len(pre_time),len(time)))
##for i in range(len(pre_time)):
##    positive_trace[i] = stdp.updateTracePre(pre_time[i], post_time)
##
##np.savetxt(positive_update_trace_path, positive_trace, \
##               fmt = '%1.4e',delimiter =',')
##
##

