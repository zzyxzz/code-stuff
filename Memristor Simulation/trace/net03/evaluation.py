import numpy as np
import pylab as plt
import cmemristor as cm
import spike_generator as sp
import LifNeuron as lif
import StdpTraing as st
import random as ran
import os.path


########set the path############
rpath = 'C:/Users/xy24/Google Drive/code/\
Memristor Simulation/trace/net03/dataset/'

a_class_post_time_path = os.path.join(rpath,'actual_class_post_spike_time1')
class_post_time_path = os.path.join(rpath,'class_post_spike_time')

##read the actual class post time spike train
fa = open(a_class_post_time_path,'r')
actual_time = []

for line in fa:
    tmp = [item for item in line.split(',')]
    tmp = [float(item) for item in tmp]
    #print tmp
    actual_time.append(tmp)
fa.close()

##read the class post time spike train
fc = open(class_post_time_path,'r')
class_time = []

for line in fc:
    tmp = [item for item in line.split(',')]
    tmp = [float(item) for item in tmp]
    #print tmp
    class_time.append(tmp)
fc.close()

mse1 = []
mse2 = []
diff = []
for i in range(len(class_time)):
    a = np.array(class_time[i])
    b = np.array(actual_time[i])
    post_diff = a - b
    diff.append(post_diff)
    errorLen = len(class_time[i])
    mse = sum(np.square(post_diff))/errorLen
    mse1.append(np.sqrt(mse))

##for i in range(len(class_time)):
##    a = diff[:][i]
##    print a
##    errorlen = len(a)
##    mse = sum(np.square(a))/errorlen
##    mse2.append(np.sqrt(mse))
##    
print mse1
print diff
#print mse2
