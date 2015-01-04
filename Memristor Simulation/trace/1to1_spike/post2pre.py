import matplotlib.pyplot as plt
import numpy as np

pre  = (25,20)
post = (15,11)

barwidth = 0.5    ##width of broken bars

xticks = np.arange(0,31,10)
yticks = -np.arange(0,1.1,0.5)
#print yticks

##simulation parameters
dt = 0.025   ##steps

##trace parameters
tau = 6             ##larger tau, longer trace
time = np.arange(0, 40 + dt, dt)
A = -1          ## amplitude

##trace
def trace(det):
    tx = np.zeros(len(time))
    for i ,t in enumerate(time):
        if t >= det:
            tx[i] = A* np.exp((-t+det)/tau)
    return tx

## cal the trace
tx1 = trace(15)
bpoint = A* np.exp((-10.0)/tau)


#plt.figure()
ax1 = plt.subplot(211)

ax1.set_yticks([6,25])
ax1.set_xticks(xticks)
ax1.set_xlabel('Time Elapsed')
ax1.set_yticklabels(['Post','Pre'])
ax1.set_ylim(0,31)
ax1.set_xlim(0,40)
ax1.set_title('Depression of memrsitive synapse')
ax1.grid(True)

## pre spike bar
plt.broken_barh([(25,barwidth)],(20,10), facecolor = 'blue')
## post spike bar
plt.broken_barh([(15,barwidth)],(1,10),facecolor = 'red')

###show post spike to pre spike##
ax1.annotate('',
            xy     = pre, xycoords   = 'data',
            xytext = post,  textcoords = 'data',
            arrowprops = dict(color = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )

ax2 = plt.subplot(212)
plt.plot(time,tx1)

## fill the synaptic change area
ax2.fill_between(time, 0, tx1, where = tx1 > bpoint, facecolor = 'gray')

## drawing parameters
ax2.grid(True)
ax2.set_ylim(-1.1,0)
ax2.set_xlim(0,40)
ax2.set_xticks(xticks)
ax2.set_yticks(yticks)
ax2.set_ylabel('Spike strength')
ax2.xaxis.tick_top()

## arrow shows post spike trigers a spike trace ##
ax2.annotate('',
             xy =(15,0), xycoords = 'data',
             xytext = (15,0.35) , textcoords='data',
             arrowprops = dict(color = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
             )

## arrow shows pre spike trigers synaptic change ##
ax2.annotate('',
             xy =(25,0), xycoords = 'data',
             xytext = (25,1) , textcoords='data',
             arrowprops = dict(color = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
             )
## change height space between subplots ##
plt.subplots_adjust(hspace = 0.3)
plt.show()

