from flask import render_template
from app import app, db
from flask_login import current_user
from Library.StyleModuleF import Style
from Library.FlaskModule import Flasker
from Library.SessionModule import Sessioner

version = '1.7.1'
@app.errorhandler(404)
def not_found_error(error):
    return common_error(404, 'OOPS, URL Not Found')

@app.errorhandler(500)
def internal_error(error):
    return common_error(500, 'OOPS, Sorry Sorry Sorry')

def common_error(error, title):
    db.session.rollback()
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    style = Style()
    sstyle = style.getCommonStyle();
    tmp = 'error/' + str(error) + '.html'

    return render_template(tmp, user=current_user, flasker=Flasker(), title=title, sstyle=sstyle, cuser=cuser), error
