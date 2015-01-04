import numpy as np
import matplotlib.pyplot as plt
import scipy.io as io

matx = io.loadmat('xbipoo.mat',matlab_compatible = True)
maty = io.loadmat('ybipoo.mat',matlab_compatible = True)
x = matx['xn']
y = maty['yn']

time1 = np.arange(0, 110, 0.01)
time2 = np.arange(-110, 0, 0.01)
fitting1 =  0.9*np.exp(-time1/18)  ##delta t > 0
fitting2 = -0.4*np.exp(time2/18)    ##delta t < 0

plt.figure()
plt.scatter(x,y/max(abs(y)), facecolors = 'none', edgecolors = 'black', s = 40)

plt.plot([-110, 110],[0, 0], 'black', linewidth = 2)  ##plot x axis
plt.plot([0, 0],[-0.6, 1.1], 'black', linewidth = 2)  ##plot y axis

plt.plot(time1, fitting1, 'red', linewidth = 2)
plt.plot(time2, fitting2, 'b', linewidth = 2)

plt.xlim([-110,110])
plt.ylim([-0.6,1.1])
plt.ylabel(r'$\xi(\%)$', fontsize = 16)
plt.xlabel(r'$\Delta t$', fontsize = 16)
#plt.grid(True)
plt.show()
