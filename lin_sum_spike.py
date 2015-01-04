import numpy as np
import matplotlib.pyplot as plt

time = np.arange(-20,100,0.01)

amp_p = 1
amp_n = -0.6

tau_p = 3
tau_n = 40

tail_p = 6
tail_n = 80

spk1 = np.zeros(len(time))
spk2 = np.zeros(len(time))
spk3 = np.zeros(len(time))
spk4 = np.zeros(len(time))

th0 = np.ones(len(time))
th1 = np.ones(len(time))
th1 = -th1

shift1 = 6
shift2 = 12
shift3 = 3

for i,t in enumerate(time):
    if  -6< t <0:
        spk1[i] = amp_p * (np.exp(t/tau_p) - np.exp(-tail_p/tau_p))/\
               (1 - np.exp(-tail_p/tau_p))
    if 0 < t < 80:
        spk1[i] = amp_n * (np.exp(-t/tau_n) - np.exp(-tail_n/tau_n))/\
                  (1- np.exp(-tail_n/tau_n))

for i,t in enumerate(time):
    if  -6 + shift1< t <0 + shift1:
        spk2[i] = amp_p * (np.exp((t-shift1)/tau_p) - np.exp(-tail_p/tau_p))/\
               (1 - np.exp(-tail_p/tau_p))
    if 0 + shift1 < t < 80 + shift1:
        spk2[i] = amp_n * (np.exp(-(t-shift1)/tau_n) - np.exp(-tail_n/tau_n))/\
                  (1- np.exp(-tail_n/tau_n))

for i,t in enumerate(time):
    if  -6 + shift2< t <0 + shift2:
        spk3[i] = amp_p * (np.exp((t-shift2)/tau_p) - np.exp(-tail_p/tau_p))/\
               (1 - np.exp(-tail_p/tau_p))
    if 0 + shift2 < t < 80 + shift2:
        spk3[i] = amp_n * (np.exp(-(t-shift2)/tau_n) - np.exp(-tail_n/tau_n))/\
                  (1- np.exp(-tail_n/tau_n))

for i,t in enumerate(time):
    if  -6 + shift3< t <0 + shift3:
        spk4[i] = amp_p * (np.exp((t-shift3)/tau_p) - np.exp(-tail_p/tau_p))/\
               (1 - np.exp(-tail_p/tau_p))
    if 0 + shift3 < t < 80 + shift3:
        spk4[i] = amp_n * (np.exp(-(t-shift3)/tau_n) - np.exp(-tail_n/tau_n))/\
                  (1- np.exp(-tail_n/tau_n))

plt.figure(figsize=(8,28),dpi=100)
plt.subplot(411)
plt.title('(a)')
plt.ylabel('Vpre')
plt.xlabel('Time')
plt.plot(time,spk1,time,spk2,time,spk3,linewidth = 2)
plt.subplot(412)
plt.title('(b)')
plt.ylabel('Vpre1+Vpre2+Vpre3')
plt.xlabel('Time')
plt.plot(time, spk1 + spk2 + spk3,time,th0,'--',time,th1,'--',linewidth = 2)
plt.ylim([-1.5,1.5])
plt.subplot(413)
plt.title('(c)')
plt.ylabel('Vpre')
plt.xlabel('Time')
plt.plot(time,spk1,time,spk4,linewidth = 2)
plt.subplot(414)
plt.title('(d)')
plt.ylabel('Vpre4+Vpre5')
plt.xlabel('Time')
plt.plot(time, spk1 + spk4,time,th0,'--',time,th1,'--',linewidth = 2)
plt.ylim([-1.5,1.5])
plt.tight_layout()
##plt.savefig('results.eps',dpi=100)
plt.show()
