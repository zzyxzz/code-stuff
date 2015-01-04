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
gray = img.open('object.bmp').convert('L')     #gray1 = rgb2gray(img1)
#bw = gray.point(lambda x: 0 if x<128 else 255, '1')
u = np.array(gray.convert('F'),dtype='d')

u += np.random.normal(200.0,100.0, u.shape)

m,n = gray.size
print u.shape

uu = np.max(u)
ul = np.min(u)
u = (u-ul)/(uu-ul)*2.0 -1.0

out  = np.copy(u)

tempA = np.zeros((3,3))
tempA[0,0] =  0.001
tempA[0,1] =  0.995
tempA[0,2] =  0.001
tempA[1,0] =  0.995
tempA[1,1] =  0.995
tempA[1,2] =  0.995
tempA[2,0] =  0.001
tempA[2,1] =  0.995
tempA[2,2] =  0.001
print tempA

tempB = np.zeros((3,3))
tempB[0,0] =  0.001
tempB[0,1] =  0.001
tempB[0,2] =  0.001
tempB[1,0] =  0.001
tempB[1,1] =  0.001
tempB[1,2] =  0.001
tempB[2,0] =  0.001
tempB[2,1] =  0.001
tempB[2,2] =  0.001

Ib = 0.0

def deriv(z, t):
    z = np.reshape(z,(m,n))
    dx = -z + Ib + Bu + Ay
    return np.reshape(dx,m*n)

def sigmoid(data):
    results = 1.0/(1.0+np.exp(-1.0*data))
    return results
    
for s in range(10):
    Bu = sig.convolve2d(u,tempB,'same')
    y = func.fs(out)
    Ay = sig.convolve2d(y,tempA,'same')
        
    out   = np.reshape(out,m*n)
    out   = sint.odeint(deriv, out, time)
    out   = np.reshape(out[2,:],(m,n))

z_edge = np.copy(out)

tempA[0,0] =  0.001  
tempA[0,1] =  0.001
tempA[0,2] =  0.001
tempA[1,0] =  0.001
tempA[1,1] =  2.0
tempA[1,2] =  0.001
tempA[2,0] =  0.001
tempA[2,1] =  0.001
tempA[2,2] =  0.001

tempB[0,0] =  -0.247
tempB[0,1] =  -0.247
tempB[0,2] =  -0.247
tempB[1,0] =  -0.247
tempB[1,1] =   2.0
tempB[1,2] =  -0.247
tempB[2,0] =  -0.247
tempB[2,1] =  -0.247
tempB[2,2] =  -0.247

Ib = -1.5

for s in range(10):
    Bu = sig.convolve2d(out,tempB,'same')
    y = func.fs(z_edge)
    Ay = sig.convolve2d(y,tempA,'same')
        
    z_edge   = np.reshape(z_edge,m*n)
    z_edge   = sint.odeint(deriv, z_edge, time)
    z_edge   = np.reshape(z_edge[2,:],(m,n))
    
z_edge = sigmoid(z_edge)
    
plt.figure(figsize=(16,5.6), dpi = 100)
plt.subplot(131)
plt.imshow(u,cmap = cm.Greys_r)
plt.title('(a)',fontsize=16)
plt.xticks([])
plt.yticks([])
plt.xlabel('Original')

plt.subplot(132)
plt.imshow(out,cmap = cm.Greys_r)
plt.title('(b)',fontsize=16)
plt.xticks([])
plt.yticks([])
plt.xlabel('Noise removed')

plt.subplot(133)
plt.imshow(z_edge,cmap = cm.binary)
plt.title('(c)',fontsize=16)
plt.xticks([])
plt.yticks([])
plt.xlabel('Edge detected')

plt.tight_layout()
plt.show()

##out = img.fromarray(z).convert('L')
##out.save('out.bmp')


