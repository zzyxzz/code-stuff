import numpy as np
import pylab as plt
import cmemristor as cm
import spike_generator as sp
import LifNeuron as lif
import StdpTraing as st
import random as ran

##simulation parameters
dt   = 0.025
time = np.arange(0,400+dt,dt)

##Create a presynaptic spike generator 
genSpike   = sp.TraceGenerator(dt,time)
channelNum = 10

##set time of spike train
time_s0     = np.sort(ran.sample(range(1,390),11))
time_s1     = np.sort(ran.sample(range(1,390),11))
time_s2     = np.sort(ran.sample(range(1,390),11))
time_s3     = np.sort(ran.sample(range(1,390),11))
time_s4     = np.sort(ran.sample(range(1,390),11))
time_s5     = np.sort(ran.sample(range(1,390),11))
time_s6     = np.sort(ran.sample(range(1,390),11))
time_s7     = np.sort(ran.sample(range(1,390),11))
time_s8     = np.sort(ran.sample(range(1,390),11))
time_s9     = np.sort(ran.sample(range(1,390),11))

time_s = np.array([time_s0,time_s1,time_s2,time_s3,time_s4,time_s5,time_s6,time_s7,time_s8,time_s9])
print time_s0
## generate pre spike train
train = np.zeros([10,len(time)])
train[0]     = genSpike.getTrace(time_s0,1)
train[1]     = genSpike.getTrace(time_s1,1)
train[2]     = genSpike.getTrace(time_s2,1)
train[3]     = genSpike.getTrace(time_s3,1)
train[4]     = genSpike.getTrace(time_s4,1)
train[5]     = genSpike.getTrace(time_s5,1)
train[6]     = genSpike.getTrace(time_s6,1)
train[7]     = genSpike.getTrace(time_s7,1)
train[8]     = genSpike.getTrace(time_s8,1)
train[9]     = genSpike.getTrace(time_s9,1)

def sumTrain():
    total_train = np.zeros(len(time))
    for i in range(len(train)):
        total_train += train[i]
    return total_train

summedTrain = sumTrain()
        
## record the trains
f = open('pretrains','w')
for i in range(len(train)):
    f.write('Train time'+ str(i) + '\n' + str(time_s[i]) + '\n')
f.close()

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
    x = train[0]*mem0.g[t] + train[1]*mem1.g[t] + train[2]*mem2.g[t] + train[3]*mem3.g[t] + train[4]*mem4.g[t] + train[5]*mem5.g[t] + train[6]*mem6.g[t] + train[7]*mem7.g[t] + train[8]*mem8.g[t] + train[9]*mem9.g[t]
    lif      = lif.LifNeuron(dt,time)
    lifOut   = lif.getLifOut(x)   ##get output of LIF
postTime = lif.sptime
btrain   = genSpike.getTrace(postTime,-1)
print postTime

## record the trains
f = open('posttrains','w')
for i in range(len(postTime)):
    f.write('Post Train time'+ str(i) + '\n' + str(postTime[i]) + '\n')
f.close()

diff = train[0] - btrain
darea = np.trapz(diff,time)
print darea
## get the learning area for specific channel
stdp = st.StdpTraining(dt,time, genSpike)
pvm  = stdp.updatePre(time_s0, postTime)
bvm  = stdp.updatePost_rr(time_s0, postTime)
print 'pvm is ' + str(pvm) + '\n' + 'bvm is ' + str(bvm) + '\n' 

##update memristor

for i,t in enumerate(time):
    if t > 0:
        mem0.calPhi(i, np.sin(t))
        mem0.calCharge_cubic(i)
        mem0.memPw(i)
    else:
        if i > 0:
            mem0.keepPre(mem0.q[i-1], mem0.phi[i-1], mem0.g[i-1],i)


##plt.figure()
##plt.subplot(312)
##plt.scatter(time, Imem, s = 0.5)
##plt.ylabel("Imem")
##plt.xlabel("time")
##plt.grid(True)

##plt.scatter(time, mem.r, s = 0.5)
##plt.ylabel("Rmem")
##plt.xlabel("Time")
##plt.grid(True)
##
##plt.figure()
###plt.scatter(time, mem.phi, s = 0.5)
##plt.scatter(mem.phi, mem.q, s = 0.5, color = 'b')
##plt.grid(True)
plt.figure()
plt.plot(time, lifOut)

plt.figure()
plt.subplot(311)
plt.plot(time,train[0])
plt.subplot(312)
plt.plot(time,btrain)
plt.subplot(313)
plt.plot(time,diff)
plt.show()

#trace1.printTrace()
