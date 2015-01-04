import numpy as np

x  = np.array([[0,0],[0,1],[1,0],[1,1]])
zt = np.array([[0,0],[1,0],[0,1],[0,0]])
w1 = np.array([0.1,0.8])
w2 = np.array([-0.5,-0.4])
for t in range(20):
    win = 0
    for i in range(4):
        print i
        z1 = np.dot(x[i],w1.T)
        z2 = np.dot(x[i],w2.T)

        if z1 > 0 :
            z1 = 1
        else:
            z1 = 0
        if z2 > 0:
            z2 = 1
        else:
            z2 = 0
        out=np.array([z1,z2])
    
##        w1 =  w1 + 0.2*np.multiply(x[i],(zt[i][0] - z1))
##        w2 =  w2 + 0.2*np.multiply(x[i],(zt[i][1] - z2))
        w1 =  np.multiply(zt[i][0],(x[i]-w1))
        w2 =  np.multiply(zt[i][1],(x[i]-w2))
        p = zt[i] -out
        print p
        if p[0] == 0 and p[1]==0:
            win = win +1
        if win == 4:
            print 'Win----------------------'
            print w1
            print w2
print '------------'
print w1
print w2
        

