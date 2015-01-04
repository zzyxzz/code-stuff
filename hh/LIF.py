import numpy as np
import matplotlib.pyplot as plt

#set parameters
T = 500 #total simulation time
dt = 0.2 #time step
time = np.arange(0,T+dt,dt) #time array
t_rest = 0 #initial refractory time

#LIF
Vm = np.zeros(len(time)) #potential trace over time
Vm_out = np.zeros(len(time))
Rm = 1 #R
Cm = 10#C
tm = Rm*Cm
t_ref = 1 #refractory period
Vthr = 1 #spike threshold
V_spike = 1

##stimulus
I = 1.5 #current

###st1 = np.random.normal(0,3,len(time)) ##normal distribution
##st1 = np.random.poisson(1.5,len(time))
##st1 = abs(st1)*0.9                     ##random number

##iterate over time step
for i, t in enumerate (time):
    if t>t_rest:
        Vm[i]=Vm[i-1]+(-Vm[i-1]+I*Rm)*dt/tm
        if Vm[i]>Vthr:
            Vm[i]+=V_spike
            t_rest = t+t_ref
t_rest = 0
for i, t in enumerate (time):
    if t>t_rest:
        Vm_out[i]=Vm_out[i-1]+(-Vm_out[i-1]+Vm[i]*Rm*1.5)*dt/tm
        if Vm_out[i]>Vthr:
            Vm_out[i]+=V_spike
            t_rest = t+t_ref
            
##plot
plt.figure()
plt.subplot(211)
plt.plot(time,Vm)
plt.title('LIF')
plt.ylabel('voltage')
plt.xlabel('time')
plt.ylim([0,2])

plt.subplot(212)
plt.plot(time, Vm_out)
plt.title('output neuron')
plt.show()
