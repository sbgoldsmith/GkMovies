import time
import logging
import inspect
from flask_login import current_user

TIMER = 25

def getMsg(nextFrame, message):
    nextFrame1 = nextFrame[1]

    py = nextFrame1[1]
    lineNo = str(nextFrame1[2])
    func = nextFrame1[3]

    bs = py.rfind('\\')
    py = py[bs+1:len(py)]
    
    if current_user and current_user.is_authenticated:
        us = current_user.login + ' '
    else:
        us = ''

        
    msg = us + py + ':' + func + '(' + lineNo + ') ' + message
    return msg
    
    
def debug(message):
    curFrame = inspect.currentframe()
    nextFrame = inspect.getouterframes(curFrame, 2)  
    msg = getMsg(nextFrame, message)
    
    logging.getLogger('gk').debug(msg)
    
def info(message=''):
    curFrame = inspect.currentframe()
    nextFrame = inspect.getouterframes(curFrame, 2)  
    msg = getMsg(nextFrame, message)

    logging.getLogger('gk').info(msg)
    

def prt(name, obj):   
    print ('@@@ ' + name)
    print (obj)
    

class Timer:
    def __init__(self):
        self.time = int(round(time.time() * 1000))

    def elapse(self, strg):
        newTime = int(round(time.time() * 1000))
        elapsed = newTime - self.time
        self.time = newTime
        logging.getLogger('gk').log(TIMER, strg + ': ' + str(elapsed))

        
        
        