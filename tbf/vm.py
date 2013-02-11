import time
from threading import Timer

from expr import *

class RealtimeVM():

    def __init__(self, values):
            
        def dispatchProc(callback, timeout):
            Timer(timeout, callback).start()

        for val in values.values():
            val.setDispatchProc(dispatchProc)
        for val in values.values():
            val(False)

    def run(self):
        pass

class SimulationVM():

    def __init__(self, values):
        self._t = 0
        def int_t(dt):
            self._t += dt
    
        self._dispatcher = sched.scheduler(time.time, inc_t)
 
        def dispatchProc(callback, timeout):
            self._dispatcher.enter(timeout, 1, callback, ())

        for val in values.values():
            val.setDispatchProc(dispatchProc)
        for val in values.values():
            val(False)

    def run(self):
        self._dispatcher.run()
