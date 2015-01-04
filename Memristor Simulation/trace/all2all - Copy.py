import numpy as np
import pylab as plt
import cmemristor as cm

##simulation parameters
dt = 0.025

##trace parameters
tau = 10
time = np.arange(0, 60 + dt, dt)
A = 0.2          ## amplitude

##trace
def trace(det):
    tx = np.zeros(len(time))
    for i ,t in enumerate(time):
        if t >= det:
            tx[i] = A* np.exp((-t+det)/tau)
    return tx

######################set LIF parameters##########################
T = 50 #total simulation time
dt = 0.2 #time step
time = np.arange(0,T+dt,dt) #time array
t_rest = 0 #initial refractory time

#LIF
Vm = np.zeros(len(time)) #potential trace over time
Rm = 1 #R
Cm = 10 #C
tm = Rm*Cm
#t_ref = 16 #refractory period
Vthr = 1 #spike threshold
V_spike = 0.5

##stimulus
I =1.3

sp_time = np.zeros(len(time))
##iterate over time step
def lifnueon(t_ref):
    for i, t in enumerate (time):
        if t>t_rest:
            Vm[i]=Vm[i-1]+(-Vm[i-1]+I*Rm)*dt/tm
            if Vm[i]>Vthr:
                sp_time[i] = 1
                Vm[i] += V_spike
                t_rest = t+t_ref

#########################################################################
            
mem1 = cm.memristor_flux(dt,time)
mem1.phi[0] = 5
mem1.calCharge_cubic(0)
mem1.calMem(0)
print(mem1.r[0])

mem2 = cm.memristor_flux(dt,time)
mem2.phi[0] = 6
mem2.calCharge_cubic(0)
mem2.calMem(0)
print(mem2.r[0])

mem3 = cm.memristor_flux(dt,time)
mem3.phi[0] = 6
mem3.calCharge_cubic(0)
mem3.calMem(0)
print(mem3.r[0])

##lif1 = 

for i,t in enumerate(time):
    if t > 50:
        mem1.calPhi(i, -txtotal[i])
        mem1.calCharge_cubic(i)
        mem1.calMem(i)
    else:
        if i > 0:
            mem1.keepPre(mem1.q[i-1],mem1.phi[i-1],mem1.r[i-1],i)

##plt.figure(1)
##plt.subplot(211)   ##subplot(num of rows,num of cols, fig num)
##plt.scatter(time, txtotal, s = 0.5)
####plt.title("Trace")
##plt.ylabel("Traces")
##plt.xlabel("Time")
##plt.plot([1 , 1],[0,0.1],color = 'r',linestyle='--',lw = 2)
##plt.plot([15,15],[0,0.1],color = 'r',linestyle='--',lw = 2)
##plt.plot([30,30],[0,0.1],color = 'r',linestyle='--',lw = 2)
##plt.plot([50,50],[0,0.1],color = 'b',linestyle='--',lw = 2)
##plt.grid(True)

##plt.subplot(312)
##plt.scatter(time, Imem, s = 0.5)
##plt.ylabel("Imem")
##plt.xlabel("time")
##plt.grid(True)

plt.subplot(212)
plt.scatter(time, mem1.r, s = 0.5)
plt.ylabel("Rmem")
plt.xlabel("Time")
plt.grid(True)

plt.figure(2)
plt.scatter(time, mem1.phi, s = 0.5)
plt.scatter(time, mem1.q, s = 0.5, color = 'b')
plt.grid(True)
plt.show()
