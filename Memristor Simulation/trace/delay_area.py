import pylab as plt
v1 = [0, 0, 5,  5,  0,  0]
t1 = [0, 5, 5, 25, 25, 45]

v2 = [0, 0, 5,  5,  0,  0,  5,  5,  0,  0,  5,  5,  0,  0,  5,  5,  0,  0]
t2 = [0, 5, 5, 10, 10, 15, 15, 20, 20, 25, 25, 30, 30, 35, 35, 40, 40, 45]

plt.figure(1)
sub1 = plt.subplot(211)
plt.ylabel("Current")
plt.xlabel("Time")
plt.title("(a)")
plt.ylim([-1, 6])
plt.plot(t1, v1, color = 'black', linestyle='-', lw = 2)

sub1.annotate('',xy = (5,1), xytext = (13,1.04), arrowprops = dict(facecolor = 'black', shrink = 0.05))
sub1.annotate('',xy = (25,1), xytext = (17,1.04), arrowprops = dict(facecolor = 'black', shrink = 0.05))

sub1.text(13.1, 0.7, r'$T_{tran}$', fontsize = 20)
sub1.fill_between(t1, 0, v1, facecolor = 'yellow')
plt.grid(True)

sub2 = plt.subplot(212)
plt.ylabel("Current")
plt.xlabel("Time")
plt.title("(b)")
plt.ylim([-1, 6])
plt.plot(t2, v2, color = 'black', linestyle='-', lw = 2)

sub2.annotate('',xy = (5 ,5.5), xytext = (19,5.54), arrowprops = dict(facecolor = 'black', shrink = 0.05))
sub2.annotate('',xy = (40,5.5), xytext = (25,5.54), arrowprops = dict(facecolor = 'black', shrink = 0.05))
sub2.text(20, 5.2, r'$T_{delay}$', fontsize = 20)

sub2.text(6.5,  0.3, r'$T_{w}$', fontsize = 20)
sub2.text(16.5, 0.3, r'$T_{w}$', fontsize = 20)
sub2.fill_between(t2, 0, v2, facecolor = 'yellow')

plt.grid(True)
plt.tight_layout()
#plt.subplots_adjust(hspace = 0.4)

plt.show()
