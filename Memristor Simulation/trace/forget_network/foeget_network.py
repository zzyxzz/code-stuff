import numpy as np
import pylab as plt
import flux_control_mem as fm
#import bounded_memristor as bm
import spike_generator as sp
import LifNeuron as lif
import StdpTraing as st
import random as ran
import os.path


#####################
# simulation setting
#####################
dt = 0.05                    ##resolution
time = np.arange(0,1500+dt,dt)   ##simulation time (400) seconds

con_sti = 5

#####################
# create LIF neurons
#####################
food_neuron  =lif.LifNeuron(dt,time) 
sound_neuron = lif.LifNeuron(dt,time)
saliv_neuron = lif.LifNeuron(dt,time)

######################################
#create one synapse and set it to off
######################################
mem_s2 = fm.memristor(dt,time)
mem_s1 = 7


#######################################
#create spike generator
#######################################
genSpike   = sp.TraceGenerator(dt,time)

############################
#Training parameters
############################
food_tr  = np.zeros(len(time))
sound_tr = np.zeros(len(time))
saliv_tr = np.zeros(len(time))
saliv_trace = np.zeros(len(time))


########################### get the LIF output of the food and sound neurons #####
for i,t in enumerate(time):
    if t < 80:
        food_tr[i] = food_neuron.getLifOutOL(con_sti, i, t)
    if 100 <t <180:
        sound_tr[i] = sound_neuron.getLifOutOL(con_sti, i, t)
    if 200 < t < 880:
        food_tr[i] = food_neuron.getLifOutOL(con_sti, i, t)
        sound_tr[i] = sound_neuron.getLifOutOL(con_sti, i, t)
    if 900< t < 1500:
        sound_tr[i] = sound_neuron.getLifOutOL(con_sti, i, t)

food_sp = food_neuron.sptime  ###spike timing
sound_sp = sound_neuron.sptime

print len(sound_sp)

food_trace = genSpike.getTraceNearest(food_sp) ##get trace
sound_trace = genSpike.getTraceNearest(sound_sp)
#print food_sp
#print sound_sp

############################
#Network
############################

out_N3 = np.zeros(len(time))
new_len = 0
A = -0.08
tau = 7
wait_for_pre = 0
wait_for_post = 0
index = 16
count = 0
countn = 0
f = 12
ff = 12
n=1
nn=1

for i,t in enumerate(time):
    len_sp = len(saliv_neuron.sptime)
    if t < 80:   ##probing
        out_N1 = food_trace[i] * mem_s1
        out_N2 = 0 
        saliv_tr[i] = saliv_neuron.getLifOutOL(out_N1 + out_N2, i, t)
        
    if 100< t < 180:
        out_N1 = 0
        out_N2 = sound_trace[i]* mem_s2.g

    if 200 < t < 880: ##training
        out_N1 = food_trace[i] * mem_s1
        out_N2 = sound_trace[i] * mem_s2.g[i-1]
        saliv_tr[i] = saliv_neuron.getLifOutOL(out_N1 + out_N2, i, t)
        new_len = len(saliv_neuron.sptime)
        if t == 200 + n*100:
            f = count/1
            count = 0
            n = n+1
        if len_sp < new_len: ##new post spike arrived
            #print saliv_neuron.sptime[new_len-1]
            count = count + 1
            #print str(count)
            saliv_trace[i] = -(np.exp(-0.5*((f/3)**2)))*np.exp((-t+saliv_neuron.sptime[new_len-1])/tau)
            if wait_for_post == 1:
                mem_s2.cal_g(sound_trace[i], i)
                #print 'g up1'
            wait_for_pre = 1
            wait_for_post = 0
        else:
            saliv_trace[i] = -(np.exp(-0.5*((f/3)**2)))*np.exp((-t+saliv_neuron.sptime[new_len -1])/tau)
            if wait_for_pre == 1 and t> sound_neuron.sptime[index -1]:
                mem_s2.cal_g(sound_trace[i], i)
                #print 'g up2'
                
        if index < len(sound_neuron.sptime):
            if t >= sound_neuron.sptime[index]:
                #print str(index)
                index = index +1
                sound_trace[i] = (1-np.exp(-0.5*((f/7)**2)))*np.exp((-t+sound_neuron.sptime[index -1])/tau)
                if wait_for_pre == 1:
                    mem_s2.cal_g(saliv_trace[i], i)
                    #print 'g down 1'
                    wait_for_post = 1
                    wait_for_pre = 0
            else:
                sound_trace[i] = (1-np.exp(-0.5*((f/7)**2)))*np.exp((-t+sound_neuron.sptime[index -1])/tau)
                if wait_for_post == 1 and t >= saliv_neuron.sptime[new_len - 1]:
                    mem_s2.cal_g(saliv_trace[i], i)
                    #print 'g down 2'
        if mem_s2.g[i] == 2:
            mem_s2.keep_pre(i)
                
    if 880 <= t <= 900:  ##probing
        mem_s2.keep_pre(i)
        out_N1 = 0
        out_N2 = sound_trace[i] * mem_s2.g[i]
        saliv_tr[i] = saliv_neuron.getLifOutOL(out_N1 + out_N2, i, t)

    if 900 < t < 1500:
        out_N1 = 0
        out_N2 = sound_trace[i] * mem_s2.g[i-1]
        saliv_tr[i] = saliv_neuron.getLifOutOL(out_N1 + out_N2, i, t)
        new_len = len(saliv_neuron.sptime)
        if t == 200 + nn*100:
            ff = countn/1
            countn = 0
            nn = nn+1
        if len_sp < new_len: ##new post spike arrived
            #print saliv_neuron.sptime[new_len-1]
            countn = countn + 1
            #print str(count)
            saliv_trace[i] = -(np.exp(-0.5*((ff/3)**2)))*np.exp((-t+saliv_neuron.sptime[new_len-1])/tau)
            if wait_for_post == 1:
                mem_s2.cal_g(sound_trace[i], i)
                #print 'g up1'
            wait_for_pre = 1
            wait_for_post = 0
        else:
            saliv_trace[i] = -(np.exp(-0.5*((ff/3)**2)))*np.exp((-t+saliv_neuron.sptime[new_len -1])/tau)
            if wait_for_pre == 1 and t> sound_neuron.sptime[index -1]:
                mem_s2.cal_g(sound_trace[i], i)
                #print 'g up2'
                
        if index < len(sound_neuron.sptime):
            if t >= sound_neuron.sptime[index]:
                #print str(index)
                index = index +1
                sound_trace[i] = (1-np.exp(-0.5*((ff/7)**2)))*np.exp((-t+sound_neuron.sptime[index -1])/tau)
                if wait_for_pre == 1:
                    mem_s2.cal_g(saliv_trace[i], i)
                    #print 'g down 1'
                    wait_for_post = 1
                    wait_for_pre = 0
            else:
                sound_trace[i] = (1-np.exp(-0.5*((ff/7)**2)))*np.exp((-t+sound_neuron.sptime[index -1])/tau)
                if wait_for_post == 1 and t >= saliv_neuron.sptime[new_len - 1]:
                    mem_s2.cal_g(saliv_trace[i], i)
                    #print 'g down 2'
        if mem_s2.g[i] == 2:
            mem_s2.keep_pre(i)

plt.figure()
plt.subplot(411)
plt.plot(time,food_tr)
plt.subplot(412)
plt.plot(time,sound_trace)
plt.subplot(413)
plt.plot(time, saliv_trace)
plt.subplot(414)
plt.plot(time, mem_s2.g)
##plt.figure()
##plt.plot(sound_sp,'r*', saliv_neuron.sptime, 'bo' )
plt.show()
     
