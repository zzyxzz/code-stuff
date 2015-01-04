import numpy as np
import scipy.signal as sig
import scipy.integrate as sint 
import pylab as plt
from func import func
import matplotlib.image as mpimg
import Image as img
import ImageDraw
import matplotlib.cm as cm

T  = 1.0
dt = 0.5
time = np.arange(0,T+dt,dt)
print time
###################
# read a pic
###################
gray = img.open('lena.bmp').convert('L')     #gray1 = rgb2gray(img1)
u = np.array(gray.convert('F'),dtype='d')

f = open('u','w')
f.write('u is ' + str(u))
f.close()

m,n = gray.size
print u.shape

##uu = np.max(u)
##print uu
##ul = np.abs(np.min(u))
##print ul
##u = (u-ul)/(uu-ul)*2 -1
u = u/255
print np.min(u)

z  = np.copy(u)

tempA = np.zeros((3,3))

tempA[0,0] = -1.0
tempA[0,1] =0.0
tempA[0,2] = -1.0
tempA[1,0] = 0.0
tempA[1,1] = 4.0
tempA[1,2] = 0.0
tempA[2,0] = -1.0
tempA[2,1] = 0.0
tempA[2,2] = -1.0

print tempA

Bu = sig.convolve2d(u,tempA,'same','fill')
plt.imshow(Bu,cmap = cm.Greys_r)
plt.show()
