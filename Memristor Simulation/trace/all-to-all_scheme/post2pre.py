import matplotlib.pyplot as plt

pre  = [(35,20)]
post = [(10,11),(20,11),(30,11)]

#plt.figure()
ax = plt.subplot(111)

ax.set_yticks([6,25])
ax.set_xlabel('Time Elapsed')
ax.set_yticklabels(['Post','Pre'])
ax.set_ylim(0,31)
ax.set_xlim(0,45)
ax.set_title('Post to Pre')
ax.grid(True)

plt.broken_barh([(35,1)],(20,10), facecolor = 'blue')
plt.broken_barh([(10,1),(20,1),(30,1)],(1,10),facecolor = 'red')

for i in range(len(post)):
    ax.annotate('',
            xy=(35,20),     xycoords   = 'data',
            xytext=post[i], textcoords = 'data',
            arrowprops = dict(facecolor = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )

plt.show()

