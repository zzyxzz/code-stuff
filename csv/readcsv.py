import numpy as np
import matplotlib.pyplot as plt
import csv

time = np.linspace(0,16,3759)
d1 = []
d2 = []
with open('CH1.csv','rb') as ch1:
    data1 = csv.reader(ch1)
    for t in data1:
        d1.append(float(t[0])/10)

with open('CH2.csv','rb') as ch2:
    data2 = csv.reader(ch2)
    for t in data2:
        d2.append(float(t[0])/10)
d2 = np.array(d2)
d2 = 5.1*d2/max(d2)
plt.figure()
plt.subplot2grid((2,2),(0,0), rowspan=2)
plt.plot()
plt.title('(a)')


plt.subplot2grid((2,2),(0,1))
plt.plot(time, d1)
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
plt.ylim([1,6])
plt.title('(b)')

plt.subplot2grid((2,2),(1,1))
plt.plot(time, d2)
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
plt.ylim([-1,6])

plt.show()
