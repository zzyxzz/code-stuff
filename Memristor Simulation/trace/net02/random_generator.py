import numpy as np
import random as rd

weights = np.zeros(10)
prespike_time = np.zeros(10)  ##size can be customized

for i,t in enumerate(weights):
    weights[i] = int(rd.random()*10)/10.0
    while(weights[i]==0):
        weights[i] = int(rd.random()*10)/10.0

print weights

##for i,t in enumerate(prespike_time):
##    prespike_time[i] = rd.randint(0,400)
##
##print np.sort(prespike_time)
