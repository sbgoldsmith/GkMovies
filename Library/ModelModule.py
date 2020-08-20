from app.models import User, UserColumn
from app import db
from sqlalchemy.sql.expression import null

def addUserColumns(user):
    dfltColumns = UserColumn.query.filter(UserColumn.user_id == 1).order_by(UserColumn.srt).all()
    for dfltColumn in dfltColumns:
        newColumn = UserColumn(
                user_id = user.id,
                name=dfltColumn.name,
                label=dfltColumn.label,
                cols=dfltColumn.cols,
                rows=dfltColumn.rows,
                dataFormat=dfltColumn.dataFormat,
                vis=dfltColumn.vis,
                srt=dfltColumn.srt)

        db.session.add(newColumn)
        db.session.commit()
