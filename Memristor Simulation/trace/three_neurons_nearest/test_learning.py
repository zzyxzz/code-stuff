import numpy as np
import pylab as plt
import cmemristor as cm
#import bounded_memristor as bm
import spike_generator as sp
import LifNeuron as lif
import StdpTraing as st
import random as ran
import os.path

######this file tests the learning only using positive update trace######
######it reads a default pre spike time and a new memristor setting######
######it gets the real post spike time and real post spike trace and#####
######real positive update trace                            ######

########set the path############
rpath = 'C:/Users/xy24/Google Drive/code/\
Memristor Simulation/trace/net - Copy/dataset/'

prespike_time_path = os.path.join(rpath,'default_pre_spike_time')
postspike_time_path = os.path.join(rpath,'default_postspike_time')
d_postspike_trace_path = os.path.join(rpath,'default_postspike_trace')

positive_update_trace_path = os.path.join(rpath,'default_positive_update_trace')

##simulation parameters
dt   = 0.5 ##0.025    improve speed
time = np.arange(0,400+dt,dt)

##Create a presynaptic spike generator 
genSpike   = sp.TraceGenerator(dt,time)
channelNum = 10

################## loading data from dataset ###########

##read the default pre time spike train
f = open(prespike_time_path,'r')
pre_time = []

for line in f:
    tmp = [item for item in line.split()]
    tmp = [float(item) for item in tmp]
    #print tmp
    pre_time.append(tmp)
f.close()

##read the default post time spike train
d_post_spike_trace = np.loadtxt(d_postspike_trace_path, delimiter = ',')
print len(d_post_spike_trace)

##read the default positive update trace
d_positive_trace = np.loadtxt(positive_update_trace_path, delimiter = ',')
print len(d_positive_trace)

## generate pre spike train
train = []

for i in range(10):
    train.append(genSpike.getTrace(pre_time[i],1))

#########sum all the pre spike trace together######
#########just for test####
##
##def sumTrain():
##    total_train = np.zeros(len(time))
##    for i in range(len(train)):
##        total_train += train[i]
##    return total_train
##
##summedTrain = sumTrain()
        
###############################
# create memristors and set them
###############################

## default setting
##init_phi = [0.2, 0.7, 0.5, 0.4, 0.3, 0.25, 0.35, 0.3, 0.1, 0.6]

mem = []
init_phi = [0.5, 0.4, 0.3, 0.25, 0.35, 0.3, 0.1, 0.6, 0.2, 0.7]

for ch in range(10):
    mem.append(cm.memristor_flux(dt,time))
    mem[ch].phi[0] = init_phi[ch]
    mem[ch].calCharge_cubic(0)
    mem[ch].calMem(0)
    print mem[ch].phi[0]

#################################################
# Traning Phase setting
#################################################
loops = 50     ##traning loops
lif   = lif.LifNeuron(dt,time)       ##creat a LIF neuron
stdp = st.StdpTraining(dt,time, genSpike) ##create stdp training module
positive_trace = np.zeros((channelNum,len(time))) ##create a numpy array to save traces

#########################
# sum all the pre spikes
#########################
def sumTrain(t):
    total_train = np.zeros(len(time))
    for ch in range(len(train)):
        total_train += train[ch]*mem[ch].g[t]
        #print mem[i].g[t]
    return total_train

################################ traning starts##############################
span_area = np.zeros((channelNum, len(time))) ##SPAN ------- method

for loop in range(loops):
    ## create a LIF neuron and get the real post spikes and save them in post_time

    lif_input = sumTrain(loop)     ## get LIF input
    lifOut   = lif.getLifOut(lif_input)   ##get output of LIF
    post_time = lif.sptime
    print post_time

    ################ MSE(Mean Square Root) ###################

    ######get current post spike trace###
    r_post_spike_trace = genSpike.getTrace(post_time,-1)
    post_trace_diff = d_post_spike_trace - r_post_spike_trace
    
    errorLen = len(time)
    mse = sum(np.square(post_trace_diff))/errorLen
    print 'MSE = ' + str(mse)
    print '##########################################\n'

    ## get the learning area for specific channel
    ##generate positive update trace
    
    for ch in range(channelNum):
        positive_trace[ch] = stdp.updateTracePre(pre_time[ch], post_time) ## get current positive update trace
        span_area[ch] = np.multiply(train[ch], post_trace_diff)##SPAN ------- method
       
    trace_diff = d_positive_trace - positive_trace ##difference between positive update trace
    ################### learning #############
    for ch in range(channelNum):
        tmp_learn = np.multiply(d_post_spike_trace, trace_diff[ch])## own ---> method
        tmp_learn_err = np.trapz(tmp_learn, time)## own ----> method
        #tmp_area = np.trapz(trace_diff[ch],time)  ##integration of the positive trace difference
        span = np.trapz(span_area[ch], time)   ##SPAN -------- method
        
        #mem[ch].calPhi(loop+1, -0.05*tmp_learn_err) ##own -----> method
        #mem[ch].calPhi(loop+1, -0.05*span)  ## SPAN ----- method
        mem[ch].calPhi(loop+1, -0.05*(span+tmp_learn_err))  ####SPAN + own method
        mem[ch].calCharge_cubic(loop+1)
        mem[ch].calMem(loop+1)
        #print 'conductance' + str(ch) + ' is ' + str(mem[ch].g[loop]) + '\n'


##plt.figure()
##plt.plot(time,positive_trace,'b',pre_time[2],[0.1]*len(pre_time[2]),\
##         'b*',post_time,[0.1]*len(post_time),'ro')
##plt.show()
