import numpy as np
import pylab as plt
import cmemristor as cm
#import bounded_memristor as bm
import spike_generator as sp
import LifNeuron as lif
import StdpTraing as st
import random as ran
import os.path
from scipy.interpolate import interp1d

######this file tests the learning only using positive update trace######
######it reads a default pre spike time and a new memristor setting######
######it gets the real post spike time and real post spike trace and#####
######real positive update trace                            ######

########set the path############
rpath = 'C:/Users/xy24/Google Drive/code/\
Memristor Simulation/trace/net02/dataset/'

prespike_time_path = os.path.join(rpath,'default_pre_spike_time')
#postspike_time_path = os.path.join(rpath,'default_postspike_time')
d_postspike_trace_path = os.path.join(rpath,'default_postspike_trace')

positive_update_trace_path = os.path.join(rpath,'default_positive_update_trace')
#a_postspike_time_path = os.path.join(rpath,'actual_postspike_time')

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
#init_phi = [0.5, 0.4, 0.3, 0.25, 0.35, 0.3, 0.1, 0.6, 0.2, 0.7]
init_phi = [0.194, 0.657, 0.479, 0.415, 0.372, 0.247, 0.252, 0.363, 0.101, 0.703]
for ch in range(10):
    mem.append(cm.memristor_flux(dt,time))
    mem[ch].phi[0] = init_phi[ch]
    mem[ch].calCharge_cubic(0)
    mem[ch].calMem(0)
    print mem[ch].phi[0]

#################################################
# Traning Phase setting
#################################################
loops = 12    ##traning loops
lif   = lif.LifNeuron(dt,time)       ##creat a LIF neuron
stdp = st.StdpTraining(dt,time, genSpike) ##create stdp training module
positive_trace = np.zeros((channelNum,len(time))) ##create a numpy array to save traces

pre_weights = np.zeros(10)
after_weights = np.zeros(10)
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

#post_spike_list = []
mse1 = []
mse2 = np.zeros((channelNum,loops))
mse3 = []

timings = []

for loop in range(loops):
    ## create a LIF neuron and get the real post spikes and save them in post_time

    lif_input = sumTrain(loop)     ## get LIF input
    lifOut   = lif.getLifOut(lif_input)   ##get output of LIF
    post_time = lif.sptime
    timings.append(np.array(lif.sptime))
    print 'post time: ' + str(post_time)
    aa = np.array(post_time)
    bb = np.array([43.5, 56.0, 69.5, 90.0, 107.0, 147.5, 163.0, 269.0, 290.0, 315.0, 342.5])
    if loop == loops-1:
        timings.append(np.array([43.5, 56.0, 69.5, 90.0, 107.0, 147.5, 163.0, 269.0, 290.0, 315.0, 342.5]))
    if len(aa)==len(bb):
        mse3.append(np.sqrt(sum(np.square(aa-bb))/len(bb)))
        print 'mse3: ' + str(mse3[-1])
    ################ MSE(Mean Square Root) ###################

    ######get current post spike trace###
    r_post_spike_trace = genSpike.getTrace(post_time,-1)
    post_trace_diff = d_post_spike_trace - r_post_spike_trace
    
    errorLen = len(time)
    mse = sum(np.square(post_trace_diff))/errorLen
    mse1.append(np.sqrt(mse))
    print 'MSE out err = ' + str(mse)
    print '##########################################\n'
    
    
    ## get the learning area for specific channel
    ##generate positive update trace
    
    for ch in range(channelNum):
        positive_trace[ch] = stdp.updateTracePre(pre_time[ch], post_time) ## get current positive update trace
        span_area[ch] = np.multiply(train[ch], post_trace_diff)##SPAN ------- method
       
    trace_diff = d_positive_trace - positive_trace ##difference between positive update trace
    
    post_diff_area = np.trapz(post_trace_diff,time)
    #print post_diff_area
    ################### learning #############
    for ch in range(channelNum):

        diff = d_positive_trace[ch] - positive_trace[ch]
        mse2[ch][loop] = np.sqrt(sum(np.square(diff))/errorLen)
        
        tmp_learn = np.multiply(train[ch], trace_diff[ch])## own ---> method
        tmp_learn_err = np.trapz(tmp_learn, time)## own ----> method
        tmp_area = np.trapz(trace_diff[ch],time)  ##integration of the positive trace difference
        span = np.trapz(span_area[ch], time)   ##SPAN -------- method
        
        #mem[ch].calPhi(loop+1, -0.3*tmp_area*abs(span)) ##own -----> method  hao
        #mem[ch].calPhi(loop+1, -0.3*tmp_learn_err) ##own -----> method
        mem[ch].calPhi(loop+1, -0.4*span)  ## SPAN ----- method  hao
        #mem[ch].calPhi(loop+1, -abs(tmp_learn_err)*(span))  ####SPAN + own method
        mem[ch].calCharge_cubic(loop+1)
        mem[ch].calMem(loop+1)
        if loop == loops-1:
            print 'phi' + str(ch) + ' is ' + str(mem[ch].phi[loop]) + '\n'
            pre_weights[ch] = mem[ch].g[0]
            after_weights[ch] = mem[ch].g[loop]

print 'minium mse3 is ' + str(min(mse3))
#print timings
##plt.figure()
##plt.plot(time,positive_trace,'b',pre_time[2],[0.1]*len(pre_time[2]),\
##         'b*',post_time,[0.1]*len(post_time),'ro')
##plt.show()
target_weights = [1.13998396445,0.750831920296,0.839947366597,0.904805872198,\
                  0.995867721457,1.05826736798,0.945988941314,0.995867721457,\
                  1.43628979335,0.790420734331]            
xnew = np.linspace(0,loops-1,80)

c = abs(np.array(target_weights) - np.array(pre_weights))
d = abs(np.array(target_weights) - np.array(after_weights))


plt.figure()
plt.subplot(311)
plt.title('(a)',fontsize=14)
plt.xlabel('Iteration', fontsize=14)
plt.ylabel(r'Enhancement Error $Ew_{LTP}$',fontsize=14)
for ch in range(10):
    f2 = interp1d(range(loops),mse2[ch],kind='cubic')
    plt.plot(xnew,f2(xnew))

plt.subplot(312)
plt.title('(b)',fontsize=14)
plt.xlabel('Iteration', fontsize =14)
plt.ylabel(r'Output Error $E_{dr}$',fontsize=14)
f1 = interp1d(range(loops),mse1,kind='cubic')
plt.plot(xnew,f1(xnew))

ax=plt.subplot(313)
plt.title('(c)',fontsize=14)
plt.ylabel(r'Conductance $G$',fontsize=14)
ax.bar([1,4,7,10,13,16,19,22,25,28],pre_weights,color='b',width=1,yerr=c)
ax.bar([2,5,8,11,14,17,20,23,26,29],after_weights,color='r',width=1, yerr=d)
plt.xticks([1.5, 4.5, 7.5, 10.5, 13.5, 16.5, 19.5, 22.5, 25.5, 28.5],\
           ['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10'])
plt.xlabel('Memristive synapses',fontsize=14)

#######################################
##sth   = []
##value = []
##my_ticks = []
##tvalue = []
##
##plt.figure()
###plt.title('Training')
##plt.xlabel('Time')
##plt.ylim([0,75])
##for line in range(len(timings)):
##    line = line +1
##    tvalue.append(2*line -1)
##    tvalue.append(2*line)
##    my_ticks.append('Training '+ str(line))
##    my_ticks.append(' ')
##    
##    for i in range(len(timings[line-1])):
##        sth  [:]   =[]
##        value[:]   =[]
##        
##        sth.append(timings[line-1][i])
##        sth.append(timings[line-1][i])
##        value.append(2*line -1)
##        value.append(2*line)
##
##        if line == (len(timings)):
##            plt.plot(sth,value,color = 'r',lw=2)
##        else:
##            plt.plot(sth,value,color = 'black',lw=2)
###print my_ticks
##my_ticks[-2] = 'Target'
##plt.yticks(tvalue,my_ticks)
##
##plt.tight_layout()
plt.show()
