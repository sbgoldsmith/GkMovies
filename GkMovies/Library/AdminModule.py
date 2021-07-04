from app import db
from app.models import User, UserColumn, UserMovie, UserLog
import sqlalchemy
from sqlalchemy.orm.session import Session 
from sqlalchemy import event

rows = 0

@event.listens_for(db.session, 'after_bulk_delete')
def receive_after_bulk_delete(delete_context):
    global rows
    rows = delete_context.result.rowcount

class Adminer():

    
    def deleteUser(self, login):
        rtn = []
        user = User.query.filter(User.login == login).first()
        
        global rows
        
        rows = 0 
        db.session.query(UserMovie).filter(UserMovie.user_id == user.id).delete(synchronize_session=False)
        rtn.append(('UserMovie', rows))
        
        rows = 0 
        db.session.query(UserColumn).filter(UserColumn.user_id == user.id).delete(synchronize_session=False)
        rtn.append(('UserColumn', rows))

        rows = 0 
        db.session.query(User).filter(User.id == user.id).delete(synchronize_session=False)
        rtn.append(('User', rows))
        
        rows = 0 
        db.session.query(UserLog).filter(UserLog.login == login).delete(synchronize_session=False)
        rtn.append(('UserLog', rows))
        
        db.session.commit()
        return rtn
   
            

        

        
        