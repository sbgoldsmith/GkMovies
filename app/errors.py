from flask import render_template
from app import app, db
from Library.StyleModuleF import Style

@app.errorhandler(404)
def not_found_error(error):
    style = Style()
    sstyle = style.getCommonStyle();
    title = 'OOPS, File Not Found'
    return render_template('error/404.html', title=title, sstyle=sstyle), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    style = Style()
    sstyle = style.getCommonStyle();
    title = 'OOPS, Sorry Sorry Sorry'
    return render_template('error/500.html', title=title, sstyle=sstyle), 500
