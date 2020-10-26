from flask import session
from flask_login import current_user
from Library.PagerModule import Pager
from Library.SearchModule import Searcher
from Library.StyleModuleF import Style
from Library.LoggerModule import debug
import jsonpickle

jsons = ['pager', 'searcher']
strgs = ['settings', 'settings-expire']
            
def skey(key):
    if hasattr(current_user, 'id'):
        return key + '_' + str(current_user.id)
    else:
        return key
        
        
class Sessioner():
    def __init__(self, version):
        self.version = version
        debug('version=' + version + ', session.version=' + session.get(skey('version'), ''))

    def get(self, key):
        ukey = skey(key)
        vkey = skey('version')
        
        if vkey not in session:
            session[vkey] = self.version
            self.deleteAllKeys()
            
        if session[vkey] != self.version:   
            self.deleteAllKeys()
            
        if ukey not in session:
            #
            # Create and populate new session variable
            #
            if key == 'pager':
                obj = Pager()
                session[ukey] = jsonpickle.encode(obj)
            elif key == 'searcher':
                obj = Searcher()
                session[ukey] = jsonpickle.encode(obj)          
    
        if key in jsons:
            rtn = jsonpickle.decode(session[ukey])
            return rtn
        else:      
            return session.get(ukey)
    
    def getWithArgs(self, key, args):
        obj = self.get(key)
        obj.setArgs(args)  
        self.put(key, obj)
        return obj
    
    def put(self, key, obj):
        ukey = skey(key)
        if key in jsons:
            session[ukey] = jsonpickle.encode(obj)
        else:
            session[ukey] = obj
        
    def deleteAllKeys(self):
        keys = jsons + strgs
        for key in keys:
            ukey = skey(key)
            if ukey in session:
                session.pop(ukey)

        
        
            
