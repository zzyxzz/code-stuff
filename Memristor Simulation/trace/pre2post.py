import matplotlib.pyplot as plt

pre  = [(10,20),(20,20),(30,20)]
post = [(35,11)]

#plt.figure()
ax = plt.subplot(111)

ax.set_yticks([6,25])
ax.set_xlabel('Time Elapsed')
ax.set_yticklabels(['Post','Pre'])
ax.set_ylim(0,31)
ax.set_xlim(0,45)
ax.set_title('Pre to Post')
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

plt.show()

