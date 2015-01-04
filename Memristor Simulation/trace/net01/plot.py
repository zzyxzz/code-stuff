import numpy as np
import pylab as plt
from scipy.interpolate import interp1d
out=[]
f = open('plot','r')
for line in f:
    tmp = [float(item) for item in line.split(',')]
    out.append(tmp)
f.close()

err = []
ferr = open('ordiff','r')
for line in ferr:
    tmp = [abs(float(item)) for item in line.split(',')]
    err.append(tmp)
ferr.close()

chanelerr = []
ch = open('feback.txt','r')
for line in ch:
    tmp = [abs(float(item)) for item in line.split()]
    chanelerr.append(tmp)
ch.close()

loops = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#print out
#ran = np.random.random(10)
#print ran

f1 = interp1d(range(len(loops)),err[0],kind='cubic')
xnew = np.linspace(0,len(loops)-1,80)

sth   = []
value = []
my_ticks = []
tvalue = []

plt.figure()
plt.title('Training')
plt.xlabel('Time')
for line in range(len(out)):
    line = line +1
    tvalue.append(2*line -1)
    tvalue.append(2*line)
    my_ticks.append('Training '+ str(line))
    my_ticks.append('')
    
    for i in range(len(out[line-1])):
        sth  [:]   =[]
        value[:]   =[]
        
        sth.append(out[line-1][i])
        sth.append(out[line-1][i])
        value.append(2*line -1)
        value.append(2*line)

        if line == (len(out)):
            plt.plot(sth,value,color = 'r',lw=2)
        else:
            plt.plot(sth,value,color = 'black',lw=2)
#print my_ticks
my_ticks[-2] = 'Target'
plt.yticks(tvalue,my_ticks)

plt.figure()
plt.subplot(212)
plt.xlabel('Training Time')
plt.ylabel('Error of Output')
plt.plot(xnew,f1(xnew))
plt.subplot(211)
plt.ylabel('Error of Update')
for ch in range(10):
    f2 = interp1d(range(len(loops)),chanelerr[ch],kind='cubic')
    plt.plot(xnew,f2(xnew))
plt.show()
