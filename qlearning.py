import math
import random
import cPickle as pickle
import os
import shutil

class QLearner(object):
    def __init__(self, states, actions, discount=0.9, stepsize=0.1, T=100):
        """
        
        """
        if states <= 0:
            raise ValueError("Must have at least one state")
        if actions <= 0:
            raise ValueError("Must have at least one action")
        self.Q = [ [ 0 for _ in range(actions) ] for __ in range(states) ]
        self.a = {}
        self.s = {}
        self.r = {}
        self.stepsize = stepsize
        self.discount = discount
        self.T = T
        self.trace = []
        
    def act(self, id, state):
        self.s[id] = state
        self.a[id] = self.select_action(state)
        self.r[id] = 0
        return self.a[id]
        
    def reward(self, id, amount):
        self.r[id] += amount
        
    def commit(self, id, sprime):
        s = self.s[id]
        a = self.a[id]
        r = self.r[id]
        self.learn(s,a,r,sprime)
        
    def learn(self, s, a, r, sprime, record=True):
        future = (self.discount * max(self.Q[sprime])) if sprime != None else 0
        self.Q[s][a] += self.stepsize * (r + future - self.Q[s][a])
        if record:
            self.trace.append((s,a,r,sprime))
        
    def select_action(self, state):
        p = []
        fx = lambda x: math.exp(self.Q[state][x]/self.T) 
        bolz = [ fx(a) for a in self.Q[0] ]
        tot = sum(bolz)
        for v in bolz:
            p.append(v / tot)
        tot = p[0]
        r = random.random()
        c = 0
        while tot < r:
            c += 1
            tot += p[c]
        return c
        
    def pickle_trace(self, file):
        pickle.dump(self.trace, file)
        
    def unpickle_trace(self, file):
        trace = pickle.load(file)
        for (s,a,r,sprime) in trace:
            self.learn(s,a,r,sprime,record=False)
            
    def pickle_knowledge(self, file):
        pickle.dump(self.Q,file)
    
    def unpickle_knowledge(self, file):
        self.Q = pickle.load(file)

    def __getstate__(self):
        return {'Q': self.Q, 'discount': self.discount, 'stepsize': self.stepsize, 'T': self.T}

    def __repr__(self):
        return "QLearner:\n\tstates:{}\n\tactions:{}\n\tdiscount:{}\n\tstepsize:{}\n\tT:{}".format(
            len(self.Q), len(self.Q[0]), self.discount, self.stepsize, self.T
        )
        
    def debug(self):
        for (i,state) in enumerate(self.Q):
            print "S({}) ".format(i),
            for (j,action) in enumerate(state):
                print action,
            print ""

def qsave(qfile, q):
    if os.path.exists(qfile):
        shutil.copyfile(qfile,qfile+".bak")
    fpq = open(qfile,'w+')
    pickle.dump(q, fpq)
    fpq.close()
    
def qopen(qfile):
    if not os.path.exists(qfile):
        raise IOError("Cannot Open Q File")
    fpq = open(qfile)
    q = pickle.load(fpq)
    fpq.close()
    return q
    
def new(filename, states, actions, discount, stepsize, T):
    if os.path.exists(filename):
        raise IOError("Specified Q file already exists")
    q = QLearner(states, actions, discount, stepsize, T)
    qsave(filename,q)

def learn(tracefile, qfile):
    if not os.path.exists(tracefile):
        raise IOError("Cannot Open Trace File")
    fpt = open(tracefile)
    q = qopen(qfile)
    q.unpickle_trace(fpt)
    fpt.close()
    qsave(qfile, q)

def view(qfile,debug=False):
    q = qopen(qfile)
    print q
    if debug:
        q.debug()

def setparam(qfile,**kwargs):
    q = qopen(qfile)
    valid = {'discount': float, 'stepsize': float, 'T':float}
    for key in kwargs:
        if key in valid:
            q.__dict__[key] = valid[key](kwargs[key])
    qsave(qfile, q)

def chelp(func, required,optional,usage=False):
    if usage:
        print "Usage"
    reqs = [ "<{}:{}>".format(k,f.__name__) for k,f in required ]
    opts = [ "[--{} <{}>]".format(k,f.__name__) for k,f in optional.iteritems() ]
    print "{} {} {} {}".format(sys.argv[0], func, " ".join(reqs), " ".join(opts))

def argify(required, optional):
    remainder = sys.argv[2:]    
    keyargs = {}
    posargs = []
    outargs = {}
    while len(remainder):
        v = remainder.pop(0)
        if v.find("--") == 0:
            keyargs[v[2:]] = remainder.pop(0)
        else:
            posargs.append(v)
    
    if len(posargs) < len(required):
        chelp(sys.argv[1], required, optional, True)
        raise ValueError("Missing required parameters")

    for v,rv in zip(posargs, required):
        k,f = rv
        outargs[k] = f(v)

    for k in keyargs:
        if k not in optional:
            chelp(sys.argv[1], required, optional, True)
            raise ValueError("{} is not an optional parameter".format(k))
        outargs[k] = optional[k](keyargs[k])

    return outargs

def main():
    program = {
        'new': { 
            'required': [
                ('filename', str),
                ('states', int),
                ('actions', int),
                ('discount', float),
                ('stepsize', float),
                ('T', float)
            ],
            'optional': {},
            'func': new
        },
        'learn': {
            'required': [
                ('qfile', str),
                ('tracefile', str),
            ],
            'optional': {},
            'func': learn
        },
        'set': {
            'required': [
                ('qfile', str)
            ],
            'optional': {
                'discount': float,
                'stepsize': float,
                'T': float
            },
            'func': setparam
        },
        'view': {
            'required': [
                ('qfile', str)
            ],
            'optional': {
                'debug': bool
            },
            'func': view
        }
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in program:
        print "Usage: Any one of these commands"
        for k in program:
            chelp(k,program[k]['required'],program[k]['optional'])                
        exit(1)

    p = program[sys.argv[1]]
    v = argify(p['required'],p['optional'])
    p['func'](**v)

if __name__ == "__main__":
    import sys
    main()
