import math
p = 0
pb = 0
r  = 11
mean = 12
for i in range(r+1):
    p = (mean**i)*math.exp(-mean)
    if i > 0:
        for t in range(1,i+1):
            p = p/t
            ##print t
    pb = pb + p
    print " propability of "+ str(i)+ " is " +str(p)

pd = 1 - pb
print pb
print pd        
