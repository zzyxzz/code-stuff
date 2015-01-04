import numpy as np
import pylab as plt
#import cmemristor as cm
import bounded_memristor as bm
import spike_generator as sp
import LifNeuron as lif
import StdpTraing as st
import random as ran
import math

##simulation parameters
dt   = 0.025 ##0.025  improve speed
time = np.arange(0,400+dt,dt)

##Create a presynaptic spike generator 
genSpike   = sp.TraceGenerator(dt,time)
##Create stdp module
stdp = st.StdpTraining(dt,time, genSpike)
##number of channels
channelNum = 10

###########################
#  pre spike samples
###########################
pre_time = [] ##pre spike samples

##read the pre time spike train
f = open('pre','r')
for line in f:
    tmp = [float(item) for item in line.split()]
    pre_time.append(tmp)
f.close()

## generate pre spike train
train = []

for ch in range(10):
    train.append(genSpike.getTrace(pre_time[ch],1))   ##pre sample trace

###############################
#  post spike samples
###############################
post_time = []  ###post spike samples

##read the post time spike train
fp = open('post', 'r')
for line in fp:
    post_time = [float(item) for item in line.split()]
fp.close()

##generate post spike train
obj_spike = genSpike.getTrace(post_time,-1)   ##post sample trace
objarea = np.trapz(obj_spike,time)
print 'obj area is ' + str(objarea)


#############################################
#  diff of obj pre and obj post spikes
#############################################
spdiff     = []
spdarea    = []

##sample_bpd = []
##t_pvm = 0
##t_bvm = 0

for ch in range(len(train)):
    spd   = train[ch] - obj_spike    ## diff of sample pre spikes and post spikes
    spda  = np.trapz(spd,time)
    spdiff.append(spd)
    spdarea.append(spda)
##    print 'here'
##    sample_pvm = stdp.updatePre(pre_time[ch], post_time)
##    sample_bvm = stdp.updatePost_r(pre_time[ch], post_time)
##    for each in sample_pvm:
##        t_pvm += each
##    for each in sample_bvm:
##        t_bvm += each
##    sample_bpd.append(t_pvm - t_bvm)

#################################
# create memristors and set them
#################################
mem = []
init_phi = [0.902, 0.566, 0.277, 0.276, 0.988, 0.338, 0.037, 0.06, 0.904, 0.574]#[0.5, 0.4, 0.3, 0.25, 0.35, 0.3, 0.1, 0.6, 0.2, 0.7]#[0.2, 0.7, 0.5, 0.4, 0.3, 0.25, 0.35, 0.3, 0.1, 0.6]

for ch in range(10):
    mem.append(bm.memristor_flux(dt,time))
    mem[ch].phi[0] = init_phi[ch]
    mem[ch].calCharge_cubic(0)
    mem[ch].calMem(0)
    
########################
#   LIF
########################

## create a LIF neuron
lif      = lif.LifNeuron(dt,time) 

#########################
# sum all the pre spikes
#########################
def sumTrain(t):
    total_train = np.zeros(len(time))
    for ch in range(len(train)):
        total_train += train[ch]*mem[ch].g[t]
        #print mem[i].g[t]
    return total_train

#########################
#define sigmoid function
#########################
def sigmoid(x):
    return math.tanh(x)       #1 / (1 + math.exp(-x))

#############################
#    training
#############################
loops      = 20   ##training times
iodiff     = np.zeros((len(train),len(time)))
iodarea    = np.zeros(len(train))
#ordarea   = np.zeros(len(time))
errarea    = np.zeros(len(train))
farea      = np.zeros((10,20))
##rt_pvm = 0
##rt_bvm = 0
##rt_bpd = []

for i in range(loops):
    pre_spike = sumTrain(i)
    
    lifOut = lif.getLifOut(pre_spike) ##get real output of LIF
    postTime = lif.sptime             ##get real post spike time train
        
    #print postTime
    out_spike   = genSpike.getTrace(postTime,-1)   ## real out spikes
    outarea = np.trapz(out_spike,time)
    print 'out area' + str(outarea)
    
    ## record the real trains
    f = open('outpost','a')
    f.write(str(postTime)+'\n')
    f.close()

    ###########################################################
    # cal the diff of objected post spikes and real post spikes
    ###########################################################
    ordiff  = obj_spike - out_spike
    ordarea = np.trapz(ordiff,time)
    print 'ordarea is ' + str(ordarea)
    if -0.01 <ordarea <0.01:
        print 'stop'
        for ch in range(len(train)):
            print mem[ch].phi[i]
        
    ###################################################
    #  cal the diff of sample pre and real post spikes
    ###################################################
    for ch in range(len(train)):
        iodiff[ch]     = train[ch] - out_spike  ##add current channel diff to list
        iodarea[ch]    = np.trapz(iodiff[ch],time)
        
        err      = train[ch]*ordiff            #train[ch]*ordiff
        errarea[ch] = np.trapz(err,time)
        farea[ch,i] = errarea[ch]
    print 'errarea[0] is ' + str(errarea[0])
    ###################################################
    #get pvm and bvm
    ###################################################
    ###bvm and pvm of real data
##    rt_bpd[:] = []  ##empty the list
##
##    for ch in range(len(train)):
##        ## get the learning area for specific channel
##        real_pvm = stdp.updatePre(pre_time[ch], postTime)
##        real_bvm = stdp.updatePost_rr(pre_time[ch], postTime)
##        for each in real_pvm:
##            rt_pvm += each
##        for each in real_bvm:
##            rt_bvm += each
##        rt_bpd[ch] = rt_pvm - rt_bvm
##        ##print 'pvm is ' + str(pvm) + '\n' + 'bvm is ' + str(bvm) + '\n' 

    ###################################################
    #    update memristor  ---- STDP only(sample diff)
    ###################################################
    for ch in range(len(train)):
        mem[ch].calPhi(i+1, 0.5*(-errarea[ch]))
        mem[ch].calCharge_cubic(i+1)
        mem[ch].calMem(i+1)
    print 'conductance ' + str(mem[0].g[i]) + '\n'

#############################################
#  update memristor -----STDP + ERR(obj-out)
#############################################


for ch in range(10):
    ## record the real trains
    fe = open('fe','a')
    fe.write(str(farea[ch])+'\n')
    fe.close()
############################
# plot
############################
##plt.figure()
##plt.title('Neuron output')
##plt.plot(time, lifOut)
##
##plt.figure()
##plt.title('Mem conductance')
##plt.plot(time, mem[0].g)
###plt.ylim([0,2])
##
##plt.figure()
##plt.title('Spikes')
##plt.subplot(311)
##plt.plot(time,train[0])
##plt.subplot(312)
##plt.plot(time,obj_spike)
##plt.subplot(313)
##plt.plot(time,out_spike)
##plt.show()

#trace1.printTrace()
