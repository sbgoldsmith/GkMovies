import time
import logging

TIMER = 15

class Timer:
    def __init__(self):
        self.time = int(round(time.time() * 1000))

    def elapse(self, strg):
        newTime = int(round(time.time() * 1000))
        elapsed = newTime - self.time
        self.time = newTime
        logging.getLogger('gk').log(TIMER, strg + ': ' + str(elapsed))

        
        
        