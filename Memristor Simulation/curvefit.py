import numpy as np
from scipy.optimize import leastsq
import pylab as plt
import scipy.io as io
 
def exponent_residuals(p, y, x):
    return y - p[0] * np.exp(p[1] / x)

def exp_value(x, p):
    return p[0] * np.exp(p[1] / x)
 
p0 = [1, 1]

matx = io.loadmat('xbipoo.mat')['xn']
maty = io.loadmat('ybipoo.mat')['yn']

x = matx[2:22]
y = maty[2:22]
x = x[:,0]
y = y[:,0]

exp_plsq = leastsq(exponent_residuals, p0, args=(y, x))
print('parameter of exp', exp_plsq[0])
 
exp_err_ufunc = np.frompyfunc(lambda y, x: exponent_residuals(exp_plsq[0], y, x), 2, 1)
exp_errors = exp_err_ufunc(y, x)
exp_rms = np.sqrt(np.sum(np.square(exp_errors)))
print('rms error', exp_rms)

plt.figure()
plt.scatter(x, y, label='Origin Line')
plt.plot(x, exp_value(x, exp_plsq[0]), 'r-', label='Exponent Fitting Line')
plt.legend()
plt.grid('on')
plt.show()
