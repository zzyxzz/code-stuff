import numpy as np
import pylab as plt
import cmemristor as cm
import bounded_memristor as bm

dt = 0.025
time = np.arange(0,50+dt,dt)

I = np.sin(0.5*time)

mem = bm.memristor_flux(dt,time)

for i, t in enumerate(time):
    if i > 0:
        mem.calPhi(i,I[i])
        mem.calCharge_cubic(i)
        mem.calMem(i)

plt.figure()
#plt.plot(time,I)
plt.title('mem')
plt.scatter(time,mem.g,s=0.5)
plt.figure()
plt.scatter(mem.phi,mem.q,s=0.5)
plt.title('phi-q')
plt.show()
    
