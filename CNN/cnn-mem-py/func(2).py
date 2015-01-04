import numpy as np

class func:
####################################
#  piece-wise function
#   y = f(x) = 0.5*(|x+1| - |x-1|)
####################################
    @staticmethod
    def fs(xstate):
        x = xstate
        y = (abs(x + 1.0)- abs(x - 1.0))/2.0
        return y

if __name__ == '__main__':
    a = func()
    t = np.arange(0,1,0.1)           ##input should be numeric array not list
    b = func.fs(t)
    print b
