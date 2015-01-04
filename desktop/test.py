import numpy as np
import matplotlib.pyplot as plt

##time = np.arange(-5,100,0.01)
##
##spk = np.zeros(len(time))
##spk1 = np.zeros(len(time))
##spk2 = np.zeros(len(time))
##
##d = 5.0 * (np.exp(-10.0/12))
##print d
##
##for i,t in enumerate(time):
##    #if 0<t<60:
##        spk[i] = 5.0 * (np.exp(-t/12.0))
##    #if 0<t-10<60:
##        spk1[i] = 5.0 * (np.exp(-(t-10)/12.0))
##        spk2[i] = (5.0+d) * (np.exp(-(t-10)/12.0))
##
##
##plt.figure()
##plt.plot(time, spk+spk1)
##plt.plot(time,spk2)
##plt.show()

s = np.arange(0,1,0.001)

ron = 1
roff = 0.1

r = s*ron+(1-s)*roff

plt.plot(s,1/r)
plt.show()
