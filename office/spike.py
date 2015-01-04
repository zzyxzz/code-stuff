import math
import numpy as np
import pylab as plt

tn1 = 5
tn2 = 8
tp = 10
time = np.arange(0,20,0.05)
s = np.zeros(len(time))

for i,t in enumerate(time):
    if tn1 < t < tn2:
        s[i] = math.exp(-(t-tn1)/tp)**2
    if t >= tn2:
        s[i] = math.exp(-(t-tn2)/5)**2

plt.figure()
plt.plot(time,s)
plt.show()
