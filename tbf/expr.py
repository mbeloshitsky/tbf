import operator

class NoDispatcherError(Exception):
    pass

class ObservableValue:
    def __init__(self):
        self._old_v = None
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def __call__(self, v):
        self.notify(v)

    def notify(self, v):
        if v == self._old_v: # Lazyness
            return           # optimization
        self._old_v = v
        for o in self.observers:
            o(v)

class Fold(ObservableValue):

    def __init__(self, foldFunc, foldOne):
        ObservableValue.__init__(self)

        self._operands = []
        self._cache    = []

        self._foldFunc = foldFunc
        self._foldOne  = foldOne

    def add_operand(self, operand):
        def closure(op, i):
            def setCache(v):
                self._cache[i] = v
                self._recalc()
            op.subscribe(setCache)
        self._cache.append(False)
        closure(operand, len(self._cache)-1)
    
    def __call__(self, v):
        self._recalc()

    def _recalc(self):
        self.notify(reduce(self._foldFunc, self._cache, self._foldOne))

And = lambda : Fold(operator.and_, True) 
Or  = lambda : Fold(operator.or_, False) 

class Not(ObservableValue):
    def __init__(self, inp):
        ObservableValue.__init__(self)
        self._inp = inp
        self._inp.subscribe(self)

    def __repr__(self):
        return u"Not(%s)" % repr(self._inp)

    def __call__(self, v):
        self.notify(not v)

class TimedValue(ObservableValue):
        
    def __init__(self, timeRise, timeFall):

        ObservableValue.__init__(self)
        
        if timeRise <= 0:
            timeRise = 2
        if timeFall <= 0:
            timeFall = 2
        self._delays = {
            True  : timeRise/1000.0,
            False : timeFall/1000.0
            } 
        self._timeRise      = timeRise
        self._dispatchProc  = None
    
    def __repr__(self):
        return u"TimedValue(%d,%d) " % (self._delays[True], self._delays[False])

    def setDispatchProc(self, dispatchProc):
        self._dispatchProc = dispatchProc

    def __call__(self, v):
        if self._dispatchProc == None:
            raise NoDispatcherError()
        def closure(v, delay):
            self._dispatchProc(lambda : self.notify(v), delay)
        closure(v, self._delays.get(v, 0))
