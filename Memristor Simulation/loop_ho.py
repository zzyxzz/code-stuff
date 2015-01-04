import numpy as np
import pylab as plt

Ron = 100.0
Roff = 16000.0
Uv = 100.0
D = 1.0

R0 = Roff
Q0 = (D**2)/(Uv*Ron)
dt = 0.01

time = np.arange(0, 4+dt, dt)

v = 1.0*np.sin(0.8*np.pi*time)

phi = np.zeros(len(v))
print Q0*(R0**2)/(2*(Roff-Ron))

for i,t in enumerate(v):
    if i >0:
        phi[i] = phi[i-1]+(v[i-1] + v[i])*dt/2

p1 = (v/R0)
p2 = (1/(np.sqrt(1-2*(Roff-Ron)*phi/(Q0*(R0**2)))))
i = p1/p2

plt.plot(v,i)
#plt.plot(phi)
plt.show()
