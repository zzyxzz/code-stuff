import numpy as np
import pylab as plt

time = np.arange(-10,10,0.01)
zeros = np.zeros(len(time))


y = np.sinh(time)

plt.plot(time,y)
plt.plot(time,zeros,'black')
plt.plot(zeros,y,'black')
plt.xlabel('Voltage V')
plt.ylabel('dg/dt')
plt.xticks([])
plt.yticks([])
plt.show()
