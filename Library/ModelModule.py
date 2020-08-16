from app.models import User, UserColumn
from app import db
from sqlalchemy.sql.expression import null

def addUserColumns(user):
    userColumns = UserColumn.query.filter(UserColumn.user_id == 1).order_by(UserColumn.srt).all()
    for userColumn in userColumns:
        newColumn = UserColumn(user_id = user.id,
                name=userColumn.name,
                label=userColumn.label,
                width=userColumn.width,
                vis=userColumn.vis,
                srt=userColumn.srt)

        db.session.add(newColumn)
        db.session.commit()
