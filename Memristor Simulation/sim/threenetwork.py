from __future__ import division
from cmemristor import memristor
from chh_neuron import neuron
#from stdp_con import controller
#from trans import trans
import numpy as np
import pylab as plt

## Parameters and object creation ##    
T    = 55                #ms
dt   = 0.025             #ms

nthreshold = - 100      ##negtive threshold
pthreshold =   100      ## postive threshold

time = np.arange(0,T+dt,dt)
nnn1 = neuron(T,dt,time)
nnn2 = neuron(T,dt,time)
nnn3 = neuron(T,dt,time)

##ccc  = controller(time)
mmm1 = memristor(dt, time)
mmm2 = memristor(dt, time) 

## outputs of neurons ##
V1  = np.zeros(len(time))
V2  = np.zeros(len(time))
V3  = np.zeros(len(time))

## output current of 2 pre-neurons
Iin1 = np.zeros(len(time))
Iin2 = np.zeros(len(time))

## input current of the post-neuron ##
Ipo  = np.zeros(len(time))

## voltage on memristors and the currents ##
Im1  = np.zeros(len(time))   ##memristor current
Vdiff1 = np.zeros(len(time)) ##voltage difference on 1st memristor

Im2  = np.zeros(len(time))
Vdiff2 = np.zeros(len(time))

## Set up 1st memristor ##
mmm1.q[0] = 5
mmm1.phi_t_cubic_poly(0)
mmm1.r_t(0)
print(mmm1.r[0])

## Set up 2nd memristor ##
mmm2.q[0] = 4
mmm2.phi_t_cubic_poly(0)
mmm2.r_t(0)
print(mmm2.r[0])

## Stimulus of pre - neuron & get output ##
I1 = np.zeros(len(time))
I2 = np.zeros(len(time))
st1 = np.random.normal(0,3,1000) ##normal distribution
st1 = st1*20                      ##random number

st2 = np.random.normal(0,3,1000)
st2 = st2*20

for i, t in enumerate(time):
 if i < 1000:
     I1[i*2] = st1[i] # uA/cm2
     I2[i*2] = st2[i]
## if 20 <= t <= 24:
##     I[i] = 4                                 # uA/cm2   ###if I<3, no AP ## default value I =10
 if i > 0:
     V1[i] = nnn1.getOutput(i, I1[i-1])         #get ouput of 1st pre - neuron
     V2[i] = nnn2.getOutput(i, I2[i-1])         #get output of 2nd pre - neuron
 elif i == 0:
     V1[i] = nnn1.getOutput(i, I1[i])
     V2[i] = nnn2.getOutput(i, I2[i])
      
## Output of post - neuron & get input ##
 if i == 0:
     Iin1[i] = V1[i] / mmm1.r[i]                  ##get current from pre - neuron to post - neuron  //use previouse memristance get I
     Iin2[i] = V2[i] / mmm2.r[i]
 else:
     Iin1[i] = V1[i] / mmm1.r[i-1]
     Iin2[i] = V2[i] / mmm2.r[i-1]

 Ipo[i] = Iin1[i] + Iin2[i]
 V3[i] = nnn3.getOutput(i, Ipo[i])             ##get output from post - neuron
  
## Current ##

#### Memristor   ------  update memristance ##
## Vdiff = ccc.cal_voltage(V1[i],V2[i],i)
## if Vdiff is None :
##     mmm.rChange(mmm.r[i-1],i)
## else:
##     Im[i] = Vdiff/mmm.r[i-1]                  ##get current by voltage difference of pre - and post - neuron
##     mmm.q_t(i,Im[i])                          ##get q from current
##     mmm.phi_t_cubic_poly(i)                   ##get phi from q
##     mmm.r_t(i)                                ##get r from phi and q


#### STDP control / update memristance ####
 Vdiff1[i] = V3[i] - V1[i]
 Vdiff2[i] = V3[i] - V2[i]
 
 Vdiff1[i] = -Vdiff1[i]
 Vdiff2[i] = -Vdiff2[i]

 if Vdiff1[i] > pthreshold or Vdiff1[i] < nthreshold:
     Im1[i] = Vdiff1[i]/mmm1.r[i-1]
     mmm1.q_t(i, Im1[i])
     mmm1.phi_t_cubic_poly(i)
     mmm1.r_t(i)
 else:
     if i > 0:
         mmm1.keepPre(mmm1.q[i-1], mmm1.phi[i-1], mmm1.r[i-1], i)
 if Vdiff2[i] > pthreshold or Vdiff2[i] < nthreshold:
     Im2[i] = Vdiff2[i]/mmm2.r[i-1]
     mmm2.q_t(i,Im2[i])
     mmm2.phi_t_cubic_poly(i)
     mmm2.r_t(i)
 else:
     if i > 0:
         mmm2.keepPre(mmm2.q[i-1], mmm2.phi[i-1], mmm2.r[i-1], i)

## Plot graph ##
plt.figure()
plt.scatter(time, V1, s = 0.5, color = 'b')
plt.scatter(time, V2, s = 0.5, color = 'y')
#plt.ylim([-5,20])
#plt.xlim([10,20])
plt.title('Output of Pre- and post Neuron')

plt.scatter(time, V3, s = 0.5, color = 'r')

plt.figure()
plt.scatter(time, Vdiff1, s = 0.5, color = 'b')
plt.scatter(time, Vdiff2, s = 0.5, color = 'y')
plt.title('Voltage Difference')
plt.scatter(time, Iin1, s = 0.5, color = 'r')

plt.figure()
plt.scatter(time, Iin1, s = 0.5, color = 'b')
plt.scatter(time, Iin2, s = 0.5, color = 'y')
plt.scatter(time, Ipo,  s = 0.5, color = 'r')
plt.title('Current')

plt.figure()
plt.scatter(time, mmm1.r, s = 0.5, color = 'b')
plt.scatter(time, mmm2.r, s = 0.5, color = 'y')
#plt.plot(time,Im)
plt.title('Memristance')
plt.grid(True)

##plt.figure()
##plt.scatter(mmm.q, mmm.phi,s=0.5)
##plt.ylabel('Flux-phi')
##plt.xlabel('Charge-q')

##plt.figure()
##plt.scatter(m.v,m.i,s=0.5)
##plt.ylabel('Current')
##plt.xlabel('Voltage')

plt.show()
