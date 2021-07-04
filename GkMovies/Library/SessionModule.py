from flask import session
from flask_login import current_user
from Library.PagerModule import Pager
from Library.SearchModule import Searcher
from Library.StyleModuleF import Style
from Library.LoggerModule import debug
from Library.BeanModule import Cuser
import jsonpickle
from flask_login import current_user

jsons = ['pager', 'searcher', 'cuser']
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
        debug('getting key=' + key)
        ukey = skey(key)
        vkey = skey('version')
        
        if vkey not in session or session[vkey] != self.version:
            debug('getting version key ' + vkey + ' not in session, set version and delete keys')
            session[vkey] = self.version
            self.deleteAllKeys()
      
        if ukey not in session:
            #
            # Create and populate new session variable
            #
            if key == 'pager':
                #obj = Pager()
                session[ukey] = jsonpickle.encode(Pager())
            elif key == 'searcher':
                #obj = Searcher()
                session[ukey] = jsonpickle.encode(Searcher())
            elif key == 'cuser':
                if current_user.is_authenticated:
                    session[ukey] = jsonpickle.encode(Cuser('user', current_user.id))
                else:
                    session[ukey] = jsonpickle.encode(Cuser('user', 0))
    
        if key in jsons:
            rtn = jsonpickle.decode(session[ukey])
            rtn.setInit()
            return rtn
        else:      
            return session.get(ukey)
    
    def getWithArgs(self, key, args):
        obj = self.get(key)
        obj.setArgs(args)  
        self.put(key, obj)
        return obj
    
    def put(self, key, obj):
        debug('putting ' + key + '=' + str(obj))
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

        
        
            
