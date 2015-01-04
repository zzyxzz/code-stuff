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
nthreshold = -60
pthreshold =  60
time = np.arange(0,T+dt,dt)
nnn1 = neuron(T,dt,time)
nnn2 = neuron(T,dt,time)
##ccc  = controller(time)
mmm  = memristor(dt, time)

V1  = np.zeros(len(time))
V2  = np.zeros(len(time))
Iin = np.zeros(len(time))
Im  = np.zeros(len(time))
Vdiff = np.zeros(len(time))

## Set up emristor ##
mmm.q[0] = 3
mmm.phi_t_cubic_poly(0)
mmm.r_t(0)
print(mmm.r[0])

## Stimulus of pre - neuron & get output ##
I = np.zeros(len(time))
st = np.random.normal(0,3,1000) ##normal distribution
st = st*20                      ##random number

for i, t in enumerate(time):
## if i < 1000:                    ##random use
##     I[i*2] = st[i] # uA/cm2
 if 20 <= t <= 40:
     I[i] = 10                                  # uA/cm2   ###if I<3, no AP ## default value I =10
 if i > 0:
     V1[i] = nnn1.getOutput(i, I[i-1])         #get ouput of pre - neuron
 elif i == 0:
     V1[i] = nnn1.getOutput(i, I[i])
      
## Output of post - neuron & get input ##
 if i == 0:
     Iin[i] = V1[i]/ mmm.r[i]                  ##get current from pre - neuron to post - neuron  //use previouse memristance get I
 else:
     Iin[i] = V1[i] / mmm.r[i-1]
 V2[i] = nnn2.getOutput(i, Iin[i])             ##get output from post - neuron
  
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


###### STDP control / update memristance ####
## Vdiff[i] = V2[i] - V1[i]
## Vdiff[i] = - Vdiff[i]          ######sign
## if Vdiff[i] > pthreshold or Vdiff[i] < nthreshold:
##     Im[i] = Vdiff[i]/mmm.r[i-1]
##     mmm.q_t(i, Im[i])
##     mmm.phi_t_cubic_poly(i)
##     mmm.r_t(i)
## else:
##     if i > 0:
##         mmm.keepPre(mmm.q[i-1], mmm.phi[i-1], mmm.r[i-1], i)
##

########    test only    ####  no threshold
 Vdiff[i] = V2[i] - V1[i]
 Vdiff[i] = - Vdiff[i]          ######sign
 Im[i] = Vdiff[i]/mmm.r[i-1]
 mmm.q_t(i, Im[i])
 mmm.phi_t_cubic_poly(i)
 mmm.r_t(i)

         
## Plot graph ##
plt.figure()
plt.scatter(time, V2, s=0.5, color='y')
#plt.ylim([-5,20])
#plt.xlim([10,20])
plt.title('Output of Pre- and post Neuron')

plt.scatter(time, V1, s=0.5, color = 'b')

plt.figure()
plt.scatter(time, -Vdiff, s=0.5)
plt.title('Voltage Difference')
plt.scatter(time,Iin, s= 0.5, color = 'r')

plt.figure()
plt.scatter(time,mmm.r,s=0.5)
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
