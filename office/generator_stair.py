import numpy as np 
import pylab as plt
from scipy.signal.waveforms import square 

time = np.arange(0,2*np.pi,0.025) ##simulation time
##voltage =  200*np.sin(1*2*np.pi* time)
swave = 0.1*square(0.5*np.pi*time, duty=0.5)

voltage = np.zeros(len(time))
for i,t in enumerate(voltage):
    voltage[i] = 5


dt = 0.025
current   = np.zeros(len(voltage))
charge    = np.zeros(len(voltage))
Rs  = np.zeros(len(voltage))
#Rhp = 250.0
Rs[0] = 1440.0


def stair_q_2_r(q):
    A = 0.04
    B = 0.08
    C = 0.12
    D = 0.16
    r_0 = 225.0
    r_1 = 175.0
    r_2 = 125.0
    r_3 = 75.0
    r_4 = 25.0
    
    if q < A:
      #self.phi[t] = r_0*q
      r = r_4
    elif q < B:
      #self.phi[t] = r_1*q 
      r = r_3
    elif q < C:
      #self.phi[t] = r_2*q 
      r = r_2
    elif q < D:
      r = r_1
    else:
      #self.phi[t] = r_3*q
      r = r_0
    return r

for i,v in enumerate(swave):
    if i > 0:
        current[i] = v
        charge[i] = charge[i-1] + current[i]*dt
        Rs[i] = stair_q_2_r(charge[i])
        #Rhp[i] = hp_q_2_r(charge[i])
         
vrs = current*Rs
vstair = current*160
#vhp = current*Rhp

plt.figure()
plt.subplot(211)
plt.plot(time,swave)
plt.ylabel('Current (A)')
plt.subplot(212)
plt.plot(time, vrs)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
#plt.ylim([min(vrs)-1,max(vrs)+1])
#plt.xlim([0,0.5])
plt.show()
