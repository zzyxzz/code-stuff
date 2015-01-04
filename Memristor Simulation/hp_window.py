import numpy as np 
from scipy.signal.waveforms import square 
import pylab as plt

dt = 0.025
time = np.arange(0,2*np.pi,dt)
r = np.zeros(len(time))
current = np.zeros(len(time))


q = np.zeros(len(time))
w = np.zeros(len(time))
Ron = 100.0 
Roff = 16000.0
Uv = 100 
D = 1

a = Uv*Ron/D

voltage = 0.7*np.sin(time)

for i,t in enumerate(voltage):
  if i < len(time)-1:
    r[i] = Ron*w[i]/D + Roff*(1-w[i]/D)
    current[i] = t/r[i]
    q[i+1] = q[i] + current[i]*dt
    w[i+1] = 1/(1+np.exp(-a*q[i+1]))

###window function

x = np.arange(0,1,0.001)
p = 0
fxx = []

for i in range(10):
  p = p +1
  fx = 1 - (2*x-1)**(2*p)
  fxx.append(fx)

plt.figure(figsize=(10,4.8), dpi=100)
plt.subplot(121)
plt.xlabel('Voltage', fontsize=16)
plt.ylabel('Current', fontsize=16)
plt.plot(voltage,current*1000)

plt.subplot(122)
for i in range(10):
  plt.plot(x,fxx[i])
plt.xlabel('x', fontsize=16)
plt.ylabel('f(x)', fontsize=16)

##plt.figure()
##plt.plot(time,r)

plt.tight_layout()
plt.show()
    

