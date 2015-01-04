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

tx1 = trace(1)
tx2 = trace(15)
tx3 = trace(30)

mem = cm.memristor_flux(dt,time)
mem.phi[0] = 5
mem.calCharge_cubic(0)
mem.calMem(0)
print(mem.r[0])

for i,t in enumerate(time):
    if t > 50:
        mem.calPhi(i,-tx3[i])
        mem.calCharge_cubic(i)
        mem.calMem(i)
    else:
        if i > 0:
            mem.keepPre(mem.q[i-1],mem.phi[i-1],mem.r[i-1],i)

plt.figure(1)
plt.subplot(211)   ##subplot(num of rows,num of cols, fig num)
plt.scatter(time,tx1,s = 0.5)
plt.scatter(time,tx2,s = 0.5)
plt.scatter(time,tx3,s = 0.5)
##plt.title("Trace")
plt.ylabel("Traces")
plt.xlabel("Time")
plt.plot([1 , 1],[0,0.1],color = 'r',linestyle='--',lw = 2)
plt.plot([15,15],[0,0.1],color = 'r',linestyle='--',lw = 2)
plt.plot([30,30],[0,0.1],color = 'r',linestyle='--',lw = 2)
plt.plot([50,50],[0,0.1],color = 'b',linestyle='--',lw = 2)
plt.grid(True)

##plt.subplot(312)
##plt.scatter(time, Imem, s = 0.5)
##plt.ylabel("Imem")
##plt.xlabel("time")
##plt.grid(True)

plt.subplot(212)
plt.scatter(time, mem.r, s = 0.5)
plt.ylabel("Rmem")
plt.xlabel("Time")
plt.grid(True)

plt.figure(2)
plt.scatter(time, mem.phi, s = 0.5)
plt.scatter(time, mem.q, s = 0.5, color = 'b')
plt.grid(True)
plt.show()
