import numpy as np
import matplotlib.pyplot as plt

Gon = 1
Goff = 0.1
phi_0 = 1
kp = 1
kth = -5
tau = 6
A = 5
t = np.arange(0,60,0.1)

C1 = np.exp(phi_0*kp - kth)
C2 = np.exp(-kp*A*tau*np.exp(-60/tau))
C3 = np.exp(kp*A*tau)

g = (Goff - Gon)*(1/(1+C1*C2*(C3**np.exp(-t/tau))) - 1/(1+C1))

dw = -A*tau*(np.exp(-60/tau) - np.exp(-t/tau))
x = -(np.exp(-(phi_0 +dw)**2) - np.exp(-(phi_0**2)))

plt.figure()
plt.plot(t,g)
plt.show()
