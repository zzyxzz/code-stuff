import matplotlib.pyplot as plt

pre  = [(10,20),(18,20),(23,20),(30,20),(35,20)]
post = [(15,11),(25,11)]

#plt.figure()
ax = plt.subplot(111)

ax.set_yticks([6,25])
ax.set_xlabel('Time Elapsed')
ax.set_yticklabels(['Post','Pre'])
ax.set_ylim(0,31)
ax.set_xlim(0,45)
ax.set_title('More Complex Situation (Proposed)')
ax.grid(True)

plt.broken_barh([(10,1),(18,1),(23,1),(30,1),(35,1)],(20,10), facecolor = 'blue')
plt.broken_barh([(15,1),(25,1)],(1,10),facecolor = 'red')

ax.annotate('',
            xy=(15,11),    xycoords   = 'data',
            xytext=(10,20), textcoords = 'data',
            arrowprops = dict(color = 'red', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )
for i in range(1,3):
    ax.annotate('',
            xy=(25,11),    xycoords   = 'data',
            xytext=pre[i], textcoords = 'data',
            arrowprops = dict(color = 'red', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )
    
for i in range(1,3):
    ax.annotate('',
            xy=pre[i],    xycoords   = 'data',
            xytext=(15,11), textcoords = 'data',
            arrowprops = dict(facecolor = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )
for i in range(3,5):
    ax.annotate('',
            xy=pre[i],    xycoords   = 'data',
            xytext=(25,11), textcoords = 'data',
            arrowprops = dict(facecolor = 'black', width = 1,
                              shrink = 0.05, headwidth = 4, frac = 0.05),
            )

plt.show()

