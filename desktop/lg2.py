import numpy as np
import matplotlib.pyplot as plt

x = np.array([np.log2(64),np.log2(128),np.log2(256),np.log2(512),np.log2(1024),\
                 np.log2(2048),np.log2(4096),np.log2(8192)])
y = np.array([np.log2(0.001),np.log2(0.009),np.log2(0.082),np.log2(0.747),\
              np.log2(6.955),np.log2(64.039),np.log2(606.072),np.log2(5780.868)])

A = np.vstack([x,np.ones(len(x))]).T
print A

b,c = np.linalg.lstsq(A,y)[0]
a = 2.0**c

print b*x+c
print np.log2(0.1)/np.log2(0.8)

plt.figure()
plt.plot(x,b*x+c)
plt.plot(x,y,'*')
plt.show()
