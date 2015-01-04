import numpy as np
import pylab as plt


ron  = 1.0
roff = 160.0
r    = np.arange(0,160+10,10)
r[0] = 1.0

s = np.zeros(len(r))
for i,t in enumerate(r):
    s[i] = (1.0/t - 1.0/ron)/(1.0/roff - 1.0/ron)
    print t
    print s[i]

plt.figure()
plt.plot(r,s)
plt.show()
