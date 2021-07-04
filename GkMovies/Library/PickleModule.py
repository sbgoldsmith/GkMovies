from app import db
from app.models import Pickle
import pickle



class Pickler():
    def put(self, user, obj):
        stmt = Pickle.__table__.delete().where(Pickle.user_id == user.id)
        db.session.execute(stmt)
        #db.session.commit()
        
        pick = Pickle()
        pick.user_id = user.id
        pick.pickle = pickle.dumps(obj)
        db.session.add(pick)
        db.session.commit()
        
        
    def get(self, user):
        pick = Pickle.query.filter(Pickle.user_id == user.id).first()
        obj = pickle.loads(pick.pickle)
        return obj

        
        