import numpy as np
import spike_generator as sp

class StdpTraining:
    def __init__(self, dt, time, obj):
        self.dt   = dt
        self.time = time
        self.obj = obj

    def updatePre(self, pre_times, post_times):     ##cal the pre-post pair area
        pt       = []
        area     = []
        Vm       = []
        train    = []
                
        for tb in post_times:                 ##iterate post spike times
            for tp in pre_times:              ##iterate pre  spike times
                if tp < tb:                   ##if pre spike time < post spike time
                    train.append(tp)          ##add pre spike time to train
                else:
                    break                        ###when tp > tb get out of the loop
            #print 'pre time check done'
            trace = self.obj.getTrace(train,1)##after iteration of all pre spikes get the trace for current pre-post pair
            #print 'pre trace done'
            for i, t in enumerate(self.time): ##cal the area
                if t >= tb:                   ##get all the elements after current post spike time
                    pt.append(trace[i])
            area = np.trapz(pt, dx = self.dt)        ##get current pre-post pair area
            Vm.append(area)                   ##add area to a area collection
        print 'pre done'
        return Vm

    def updateTracePre(self, pre_times,post_times): ##cal the enhance of stdp
        pre_trace = self.obj.getTrace(pre_times,1)  ##get pre-spike trace
        enhance_trace = np.zeros(len(self.time))         ##create an empty array to store the update trace
        index = 0                                   ##index of post_times
        num = 1
        for i,t in enumerate(self.time):            ##iterate the simulation time
            if(index < len(post_times) and t > post_times[index]):              ##if pre-spike trace time greater than post spike time
                if(pre_trace[i]<pre_trace[i-1]):            ##and the pre-spike trace not added(next pre spike not occured)
                    if(index+1 < len(post_times) and t > post_times[index+1]):
                        index = index+1
                        num = num +1
                        enhance_trace[i] = pre_trace[i]*num
                    else:
                        enhance_trace[i] = pre_trace[i]*num ##store(read out) the pre-spike trace
                else:
                    num = 1
                    index = index +1                ##else wait for next post spike
        return enhance_trace
        
    def updatePost(self,pre_times,post_times):             ##cal the post-pre pair area
        pt       = []
        area     = []
        bvm      = []
        train    = []
        
        for tb in post_times:
            train.append(tb)
            trace = self.obj.getTrace(train,-1)
            for tp in pre_times:
                if tp > tb:
                    for i, t in enumerate(self.time):
                        if t >= tp:
                            pt.append(trace[i])
                    area = np.trapz(pt, dx = self.dt)
                    bvm.append(area)
        print 'post done'
        return bvm

    def updatePost_r(self, pre_times, post_times):  ##restrict spike time
        pt    = []
        area  = []
        bvm   = []
        train = []

        for tb in post_times:
            train.append(tb)
            trace = self.obj.getTrace(train,-1)
            for tp in pre_times:
                if -40 <(tb - tp)< 0:
                    for i, t in enumerate(self.time):
                        if t >= tp:
                            pt.append(trace[i])
                    area = np.trapz(pt, dx = self.dt)
                    bvm.append(area)
        print 'post done'
        return bvm
    
    ##################################################
    #update depends on pre-post spike pair
    #     post|pre   or   post|pre|post
    ###################################################
    def updatePost_rr(self, pre_times, post_times):  ##restric spike pair, spike in a range
        pt    = []
        area  = []
        bvm   = []
        train = []

        for i in range(len(post_times)):
            train.append(post_times[i])
            trace = self.obj.getTrace(train,-1)
            for tp in pre_times:
                if i < len(post_times)-1:
                    if post_times[i] < tp < post_times[i + 1]:
                        for d, t in enumerate(self.time):
                            if t >= tp:
                                pt.append(trace[d])
                        area = np.trapz(pt, dx = self.dt)
                        bvm.append(area)
                else:
                    if tp > post_times[-1]:
                        for d, t in enumerate(self.time):
                            if t >= tp:
                                pt.append(trace[d])
                        area = np.trapz(pt, dx = self.dt)
                        bvm.append(area)

        print 'post done'
        return bvm

    ##di gui suan fa
    ##def compare(tb[i]):
    ##  if(tp > tb[i]):
    ##     if i < len()
    ##        compare(tb[i +1])
    ##  trace()

    def compare(self, tp, tb, train, pt):
        i = 0
        if(tp > tb[i]):
            train.append(tb[i])
            trace = self.obj.getTrace(train, -1)
            if i < len(tb)-1:
                compare(tb[i+1])
        for i, t in enumerate(self.time):
            if t >= tp:
                pt.append(trace[i])

    def updatePost_f(self, pre_times, post_times):
        pt    = []
        area  = []
        bvm   = []
        train = []

        for tp in pre_times :
            if post_times:
                self.compare(tp, post_times, train, pt)
                area = np.trapz(pt, dx = self.dt)
                bvm.append(area)
            train[:] = []
        print 'post done'
        return bvm
