import numpy as np
import scipy.signal as sig
import scipy.integrate as sint 
import pylab as plt
from func import func
import matplotlib.image as mpimg
import Image as img
import matplotlib.cm as cm
from scipy.interpolate import interp1d

T  = 1.0
dt = 0.5
time = np.arange(0,T+dt,dt)
print time
###################
# read a pic
###################
gray = img.open('lena.bmp').convert('L')     #gray1 = rgb2gray(img1)
u = np.array(gray.convert('F'),dtype='d')

m,n = gray.size
print u.shape

uu = np.max(u)
ul = np.min(u)
u = (u-ul)/(uu-ul)*2 -1

z  = np.copy(u)

tempA = np.zeros((3,3))
tempA[0,0] =  0.0
tempA[0,1] =  1.0
tempA[0,2] =  0.0
tempA[1,0] =  1.0
tempA[1,1] =  2.0
tempA[1,2] =  1.0
tempA[2,0] =  0.0
tempA[2,1] =  1.0
tempA[2,2] =  0.0
##tempA[0,0] = -1.0
##tempA[0,1] = -1.0
##tempA[0,2] = -1.0
##tempA[1,0] =  1.0
##tempA[1,1] = -2.0
##tempA[1,2] =  1.0
##tempA[2,0] =  1.0
##tempA[2,1] =  1.0
##tempA[2,2] =  1.0

print tempA

tempB = np.zeros((3,3))
print tempB

Ib = 0.0
x00 = []
x01 = []
x02 = []
x03 = []
x04 = []
x05 = []
x06 = []
x07 = []
x08 = []
x09 = []
x10 = []
x00.append(z[2,2])
x01.append(z[50,300])
x02.append(z[200,100])
x03.append(z[300,300])
x04.append(z[4,4])
x05.append(z[150,100])
x06.append(z[100,150])
x07.append(z[250,200])
x08.append(z[200,50])
x09.append(z[180,280])
x10.append(z[10,50])

def deriv(z, t):
    z = np.reshape(z,(m,n))
    dx = -z + Ib + Bu + Ay
    return np.reshape(dx,m*n)
    
for s in range(15):
    Bu = sig.convolve2d(u,tempB,'same')
    y = func.fs(z)
    Ay = sig.convolve2d(y,tempA,'same')
        
    z   = np.reshape(z,m*n)
    z   = sint.odeint(deriv, z, time)
    z   = np.reshape(z[2,:],(m,n))

    x00.append(z[2,2])
    x01.append(z[50,300])
    x02.append(z[200,100])
    x03.append(z[300,300])
    x04.append(z[4,4])
    x05.append(z[150,100])
    x06.append(z[100,150])
    x07.append(z[250,200])
    x08.append(z[200,50])
    x09.append(z[180,280])
    x10.append(z[10,50])
    #print np.max(z),np.min(z)

f0 = interp1d(range(16),x00,kind='cubic')
f1 = interp1d(range(16),x01,kind='cubic')
f2 = interp1d(range(16),x02,kind='cubic')
f3 = interp1d(range(16),x03,kind='cubic')
f4 = interp1d(range(16),x04,kind='cubic')
f5 = interp1d(range(16),x05,kind='cubic')
f6 = interp1d(range(16),x06,kind='cubic')
f7 = interp1d(range(16),x07,kind='cubic')
f8 = interp1d(range(16),x08,kind='cubic')
f9 = interp1d(range(16),x09,kind='cubic')
f10 = interp1d(range(16),x10,kind='cubic')
xnew = np.linspace(0,15,15)

#print x11
#print x22

plt.figure(figsize=(16,5.6), dpi=100)
plt.subplot(133)
p1,=plt.plot(xnew,f0(xnew),label='Cell0')
p2,=plt.plot(xnew,f1(xnew),label='Cell1')
p3,=plt.plot(xnew,f2(xnew),label='Cell2')
p4,=plt.plot(xnew,f3(xnew),label='Cell3')
p5,=plt.plot(xnew,f4(xnew),label='Cell4')
p6,=plt.plot(xnew,f5(xnew),label='Cell5')
p7,=plt.plot(xnew,f6(xnew),label='Cell6')
p8,=plt.plot(xnew,f7(xnew),label='Cell7')
p9,=plt.plot(xnew,f8(xnew),label='Cell8')
p10,=plt.plot(xnew,f9(xnew),label='Cell9')
p11,=plt.plot(xnew,f10(xnew),label='Cell10')

plt.legend(loc=7,ncol=1)
plt.title('(c)',fontsize=16)
plt.ylabel('Cell states',fontsize=16)
plt.xlabel('Time Elapsed',fontsize=16)

plt.ylim([-6.5,6.5])
plt.xlim([0,8])
#plt.grid(True)
#plt.figure()
##f = open('u','w')
##f.write('u is ' + str(z))
##f.close()
plt.subplot(132)
plt.imshow(z,cmap = cm.Greys_r)
plt.title('(b)',fontsize=16)
plt.subplot(131)
plt.imshow(u,cmap = cm.Greys_r)
plt.title('(a)',fontsize=16)

plt.tight_layout()
plt.savefig('lena_results.png',dpi=100)
plt.show()

##out = img.fromarray(z).convert('L')
##out.save('out.bmp')


