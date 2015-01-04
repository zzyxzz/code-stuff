from __future__ import division
import numpy as np
import pylab as py

################################################################################
# memristor 
################################################################################
class memristor:
  def __init__(self, sim_t, sim_dt, r_min, r_max):
    self.ts = t = np.arange(0, sim_t+dt, dt)
    self.n = len(t)
    self.r = np.zeros(len(t))
    self.v = np.zeros(len(t))
    self.i = np.zeros(len(t))
    self.phi = np.zeros(len(t)) 
    self.q = np.zeros(len(t))
    self.dt = sim_dt
    self.r_min = r_min
    self.r_max = r_max
    self.q_max = 50;
	
  def q_t(self, t):
    """ cal q(t) from i """
    if t > 0:
      self.q[t] = self.q[t-1] + self.dt*self.i[t]
    if self.q[t] > self.q_max:
      self.q[t] = self.q_max
    if self.q[t] < 0.0:
      self.q[t] = 0.0
    ##print 'q[{0}] = {1}, dt = {2}, i = {3}'.format(t-1, self.q[t-1], self.dt, self.i[t])
    ##print 'q[{0}] = {1}'.format(t, self.q[t])

  def phi_t_cubic_poly(self, t):   
    """ cal phi(t) from q """
    q = self.q[t]
    self.phi[t] = q + (q**3)/3.0

  def phi_t_pw(self, t):   
    """ cal phi(t) from q """
    B = 4.8 
    r0 = self.r_max 
    r1 = self.r_min

    q = self.q[t]
    if (q < -B):
      self.phi[t] = r1*q + (r1-r0)*B
    elif (q > B):
      self.phi[t] = r1*q + (r0-r1)*B
    else:
      self.phi[t] = r0*q

  def v_t(self, t):
    """ cal v(t) = dphi/dt """
    if t == 0:
      self.v[t] = (self.phi[t] - 0.0)/self.dt
    else:
      self.v[t] = (self.phi[t] - self.phi[t-1])/self.dt
 
  def r_t(self, t):
    """ cal v(t) = dphi/dt """
    if t > 0:
      if self.q[t] == self.q[t-1]:
        self.r[t] = self.r[t-1]
      else:
        self.r[t] = (self.phi[t] - self.phi[t-1])/(self.q[t]-self.q[t-1])
    return self.r[t]

################################################################################
## setup parameters and state variables
################################################################################
N    = 3                        # number of neurons
T    = 6600                     # total time to simulate (msec)
dt   = 1                        # simulation time step (msec)
time = np.arange(0, T+dt, dt)  # time array


## Neuron properties
Vin  = np.zeros([N,len(time)])  # Vin trace over time
Vo  = np.zeros([N,len(time)])   # Vo(utput) trace over time
Vob  = np.zeros([N,len(time)])  # backward Vo(utput) trace over time
Vth = 1.5                       # spike threshold (V)
Vf = 2.5                        # forward spike
Vb = 2.5                        # backward spike
ref = 16 #4 #20                     # refractory period (msec)

## Input Voltages
V    = np.zeros((N,len(time)))
Vext = np.zeros((N, len(time))) # externally applied stimulus
for i, t in enumerate(time[1:],1):
    '''
    Vext[0,i] = A
    Vext[1,i] = A
    '''
    A = 2.0 
    if t < 1200:
        Vext[0,i] = A 
    elif 1200 < t < 2800:
        Vext[0,i] = 0.0
    elif 2800 < t < 5200:
        Vext[0,i] = A
    else:  
        Vext[0,i] = 0.0

    if t < 1400:
        Vext[1,i] = 0.0
    elif 1400 < t < 2600:
        Vext[1,i] = A
    elif 2600 < t < 2800:
        Vext[1,i] = 0
    elif 2800 < t < 5200:  
        Vext[1,i] = A
    elif 5200 < t < 5400:
        Vext[1,i] = 0
    else:
        Vext[1,i] = A

## Network and Synapse weight matrix    
synapses = np.zeros((N, N))
synapses[2,0] = 1.0 
synapses[2,1] = 0.01

syn_trace = np.zeros([N*N,len(time)])  
syn_trace[6,0] = 1.0 
syn_trace[7,0] = 0.01 

network = synapses.nonzero();
num_conn = network[0].size;

# memristor matrix
r_min = 1
r_max = 100
r_const = 100  # ristance of the rest circuit 
mr = np.empty((N,N), dtype=np.object); 
mr[2,0] = memristor(T, dt, r_min, r_max)
mr[2,1] = memristor(T, dt, r_min, r_max)
mr[2,0].r[0] = r_min
mr[2,1].r[0] = r_max
mr[2,0].q[0] = 50
mr[2,1].q[0] = 0           #pw 
#mr[2,1].q[0] = 99**0.5     #cubic


################################################################################
# Simulation
################################################################################

## mapping for r to weight (linear)
def r2w_linear(r):
    ''' linear mapping for resistance to synapse weight'''
    min = r_min + r_const
    max = r_max + r_const

    a = 1.0/ (min - max)
    b = max / (max - min)

    if r < min:
        r = min
    if r > max:
        r = max

    w = a * r + b
    return w

## update synapses' weight
def update_synapses(step):
    ''' step is the time step from beginning'''
    for i in range(num_conn):
        post = network[0][i]
        pre = network[1][i]
        m = mr[post, pre] 

        s = post * N+pre
        syn_trace[s, step] = syn_trace[s, step - 1]

        ## fire together, wire together
        k = step 

        print k,pre,Vo[pre,k],Vob[post,k]
        s_r = m.r[k-1] + r_const
        if (Vo[pre, k] > 0 and Vob[post, k] == 0):
            m.i[k] =  2.5/s_r #1.0
        elif (Vo[pre, k] > 0 and Vob[post,k] < 0):
            m.i[k] = 20.0/s_r #2.0
        elif (Vo[pre, k] == 0 and Vob[post,k] < 0):
            m.i[k] = -2.5/s_r #2.0
        else:
            m.i[k] = 0.0
 
        m.q_t(k)
        m.phi_t_pw(k)
        #m.phi_t_cubic_poly(k)
        r = m.r_t(k) 
        print k,pre,m.i[k],r,'r'           

        synapses[post, pre] = r2w_linear(r + r_const) #1.0/r
        syn_trace[s, k] = synapses[post, pre]


## Simulate network
last_spike = np.zeros(N) - ref
spikes = np.zeros([N,len(time)])

sampling = np.zeros(N)
sampling[0] = 35 
sampling[1] = 35
sampling[2] = 20 

for i, t in enumerate(time[1:],1):
    active = np.nonzero(t > last_spike + sampling)
    print i,active
    Vin[active,i] = Vext[active,i] + (synapses[active,:]).dot(Vo[:,i])
    #print synapses
    #print 'vin: {0}, {1}, {2}'.format(Vin[0,i], Vin[1,i],Vin[2,i])
    
    ## find out firing neurons
    spiked = np.nonzero(Vin[:,i] > Vth)
    last_spike[spiked] = t
    spikes[spiked,i] = spiked[0]+1
    print i,spiked

    ## update Vo and Vob
    w = ref
    Vo[spiked,i:(i+w)] = Vf
    #Vo[spiked,i:(i+w)] = Vf
    #Vo[spiked,(i+w):(i+2*w)] = -Vf
    print i,Vo[spiked,i:(i+w)]

    Vob[spiked,i:(i+w)] = -Vb
    #Vob[spiked,i:(i+w)] = -Vb
    #Vob[spiked,(i+w):(i+2*w)] = Vb
    print i,Vob[spiked,i:(i+w)]

    ## update synapstic weight
    update_synapses(i)
    

################################################################################
# plot membrane potential trace
################################################################################

py.subplot(3,1,1)
py.plot(time, Vo[0,:])

py.subplot(3,1,2)
py.plot(time, Vo[1, :])

py.subplot(3,1,3)
py.plot(time, Vo[2, :])

#py.subplot(5,1,4)
#py.plot(time, syn_trace[7, :])
##py.plot(time, mr[2, 1].q)

#py.subplot(5,1,5)
#py.plot(time, Vext[0, :], time, Vext[1, :])
py.show()
