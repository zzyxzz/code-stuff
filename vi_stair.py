import numpy as np 
import pylab as plt

time = np.arange(0,8*np.pi,0.025) ##simulation time
current1 = 0.02 * np.sin(0.5*2*np.pi* time)
current2 = 0.02 * np.sin(4.0*2*np.pi* time)

#t = np.trapz(current)
r = np.zeros(len(time))
r[0] = 250.0

charge1 = np.zeros(len(time))
charge2 = np.zeros(len(time))
charge3 = np.zeros(len(time))

def phi_t_pw(t,q):
    A = 0.04
    B = 0.10
    C = 0.16
    D = 0.22
    r_0 = 250.0
    r_1 = 200.0
    r_2 = 150.0
    r_3 = 100.0
    r_4 = 50.0
    
    if q < A:
      #self.phi[t] = r_0*q
      r[t] = r_0
    elif q < B:
      #self.phi[t] = r_1*q 
      r[t] = r_1
    elif q < C:
      #self.phi[t] = r_2*q 
      r[t] = r_2
    elif q < D:
      r[t] = r_3
    else:
      #self.phi[t] = r_3*q
      r[t] = r_4

for i,t in enumerate(time):
      if i > 0:
        charge1[i] = charge1[i-1] + np.trapz([current1[i-1],current1[i]])
        phi_t_pw(i,charge1[i])
v1 = current1 * r

for i,t in enumerate(time):
      if i > 0:
        charge2[i] = charge2[i-1] + np.trapz([current2[i-1],current2[i]])
        phi_t_pw(i,charge2[i])
v2 = current2 * r

plt.figure()
#plt.plot(time,charge1)
plt.plot(v1,current1*1000,'r',)
plt.plot(v2,current2*1000,'b')

plt.xlabel('Voltage V (V)',fontsize = 16)
plt.ylabel('Current I (mA)',fontsize = 16)
plt.ylim([-22,22])
plt.show()
