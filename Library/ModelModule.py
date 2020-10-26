from app.models import User, UserColumn
from app import db
from datetime import datetime
from werkzeug.utils import secure_filename

class UserManager():
    def addUser(self, form):       
        user = User(login=form.login.data, 
                        email=form.email.data, 
                        firstName=form.firstName.data, 
                        lastName=form.lastName.data, 
                        city=form.city.data,
                        state=form.stateSelect.data,
                        country=form.countrySelect.data,
                        face=secure_filename(form.face.data.filename),
                        order_by='title', 
                        order_dir='asc', 
                        admin='F',
                        as_login = form.login.data, 
                        user_since = datetime.utcnow(),
                        last_visit = datetime.utcnow())
        user.set_password(form.password.data)
        db.session.add(user)
        return user
            
    def addUserColumns(self, user):
        dfltColumns = UserColumn.query.filter(UserColumn.user_id == 1).order_by(UserColumn.srt).all()
        for dfltColumn in dfltColumns:
            newColumn = UserColumn(
                    user_id = user.id,
                    name=dfltColumn.name,
                    label=dfltColumn.label,
                    displayType=dfltColumn.displayType,
                    cols=dfltColumn.cols,
                    rows=dfltColumn.rows,
                    dataFormat=dfltColumn.dataFormat,
                    vis=dfltColumn.vis,
                    srt=dfltColumn.srt)
    
            db.session.add(newColumn)

