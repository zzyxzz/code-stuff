import matplotlib.pyplot as plt
import numpy as np

pre  = [(10,20),(20,20),(30,20)]
post = [(35,11)]
######################
##trace
time = np.arange(0, 60, 0.01)

def trace(ti):
    d = np.zeros(len(time))
    for i,t in enumerate(time):
        if t - ti >=0:
            d[i] = 1.0 * np.exp(-(t - ti)/8.0)
    return d

spk1 = trace(10)
spk2 = trace(20)
spk3 = trace(30)

spk4 = trace(10)
spk5 = trace(20)
spk6 = trace(30)

spk_all = spk1 + spk2 + spk3

for i,t in enumerate(time):
    if t >= 20.0:
        spk4[i] = 0.0
    if t >= 30.0:
        spk5[i] = 0.0

spk_nearest = spk4 + spk5 + spk6

#####################
plt.figure(figsize=(8,28),dpi=100)
ax = plt.subplot(411)

ax.set_title('(a)')
ax.set_yticks([6,25])
ax.set_xlabel('Time')
ax.set_yticklabels(['Post','Pre'])
ax.set_ylim(0,31)
ax.set_xlim(0,60)
#ax.set_title('Pre to Post')
ax.grid(True)

plt.broken_barh([(10,1),(20,1),(30,1)],(20,10), facecolor = 'blue')
plt.broken_barh([(35,1)],(1,10),facecolor = 'red')

for i in range(len(pre)):
    ax.annotate('',
            xy=(35,11),    xycoords   = 'data',
            xytext=pre[i], textcoords = 'data',
            arrowprops = dict(facecolor = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )
###############
## [3500] is the index of point (time = 35)
plt.subplot(412)
plt.plot(time, spk_all)
plt.fill_between(time[3500:], 0, spk_all[3500:], facecolor = 'Tomato')
plt.xlabel('Time')
plt.title('(b)')
plt.ylim([0, 1.6])
plt.yticks([0.0,0.4,0.8,1.2])

#####################
ax1 = plt.subplot(413)

ax1.set_title('(c)')
ax1.set_yticks([6,25])
ax1.set_xlabel('Time')
ax1.set_yticklabels(['Post','Pre'])
ax1.set_ylim(0,31)
ax1.set_xlim(0,60)
#ax1.set_title('Pre to Post')
ax1.grid(True)

plt.broken_barh([(10,1),(20,1),(30,1)],(20,10), facecolor = 'blue')
plt.broken_barh([(35,1)],(1,10),facecolor = 'red')

ax1.annotate('',
            xy=(35,11),    xycoords   = 'data',
            xytext=(30,20), textcoords = 'data',
            arrowprops = dict(facecolor = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )
#################
plt.subplot(414)
plt.plot(time, spk_nearest)
plt.ylim([0,1.2])
plt.title('(d)')
plt.xlabel('Time')
plt.yticks([0.0,0.4,0.8, 1.2])
plt.fill_between(time[3500:], 0, spk_nearest[3500:], facecolor = 'Tomato')


plt.tight_layout()
plt.show()
