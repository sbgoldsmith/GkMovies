from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, SettingsAccountForm, ResetPasswordRequestForm, ResetPasswordChangeForm, AddMoviesForm, DisplayMoviesForm, UpdateForm
from app.models import User, AdderColumn
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.urls import url_parse
from app.Imdb import ImdbFind
from Library.StyleModuleF import Style
from Library.AdderModuleF import Adder
from sqlalchemy.sql import func
from Library.FlaskModule import FlaskHelper
from Library.TimerModule import Timer
from Library.ModelModule import addUserColumns
from Library.ServerModule import Inputter
from datetime import datetime, timedelta
from app.Imdb import ImdbFind
from app.email import send_password_reset_email

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    style = Style()
    sstyle = style.getCommonStyle();
    title = 'Welcome to Goldkeys Movies'
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    print("got form")
    if not form.validate_on_submit():
        if 'csrf_token' in request.form:
            # Submit button pressed
            flash('Please enter a login and password')
            
        return render_template('index.html', title=title, form=form, sstyle=sstyle)
    
    
    user = User.query.filter_by(login=form.login.data).first()
    if user is None or not user.check_password(form.password.data):
        print("invalid")
        flash('Sorry, the login / password combination was not recognized')

        return render_template('index.html', title=title, form=form, sstyle=sstyle)
    
  
    login_user(user)
    
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    
    print("redirect")
    return redirect(url_for('home'))
   

@app.route('/home')
@login_required
def home():
    style = Style()
    sstyle = style.getHomeStyle()
    
    user = User.query.filter_by(login = current_user.login).first() 
    user.setLastVisit()
    
    print(user.last_visit)
    return render_template('home.html', title='Home Page', sstyle=sstyle, user=user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    style = Style()
    sstyle = style.getCommonStyle();
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    print('in register, first.firstName=')
    print( form.firstName.__dict__)
   
        
    if form.validate_on_submit():
        user = User(login=form.login.data, 
                    email=form.email.data, 
                    firstName=form.firstName.data, 
                    lastName=form.lastName.data, 
                    order_by='title', 
                    order_dir='asc', 
                    admin='F',
                    last_visit = datetime.utcnow())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        

        addUserColumns(user)
        
        flash('Congratulations, you are now a registered user! Please login.')
        
        return redirect(url_for('index'))
    
    print('rendering')
    return render_template('register.html', title='Register', form=form, sstyle=sstyle)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    style = Style()
    sstyle = style.getCommonStyle();
    title = 'Request Password Reset'
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('index'))
    return render_template('reset_password_request.html', title=title, form=form,  sstyle=sstyle)
    
@app.route('/reset_password_change/<token>', methods=['GET', 'POST'])
def reset_password_change(token):
    style = Style()
    sstyle = style.getCommonStyle();
    title = 'Reset Your Password '
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    
    if not user:
        flash('Sorry, the password reset request has expired.  Please try again.')
        return redirect(url_for('index'))
    
    form = ResetPasswordChangeForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.  Please login to confirm.')
        return redirect(url_for('index'))
    
    return render_template('reset_password_change.html', title=title, form=form,  sstyle=sstyle)

    
@app.route('/addMovies', methods=['GET', 'POST'])
@login_required
def addMovies():
    user = User.query.filter_by(login = current_user.login).first()  
    if request.args.get('titleSearch') == None:
        titleSearch = ""
    else:
        titleSearch = str(request.args.get('titleSearch'))

    imdbFind = ImdbFind()
    movies = imdbFind.findMovies(user, titleSearch)

    style = Style()
    sstyle = style.getAdderStyle()

    form = AddMoviesForm()
    return render_template('addMovies.html', title='Add to My Movies', form=form, movies=movies, sstyle=sstyle, titleSearch=titleSearch)

@app.route('/addMovie', methods=['GET', 'POST'])
@login_required
def addMovie():
    adder = Adder()
    message = adder.addMovie(request.form['tt'])
    
    return message


@app.route('/displayMovies', methods=['GET', 'POST'])
@login_required
def displayMovies():     
    timer = Timer()

    print(request.args)
      
    user = User.query.filter_by(login = current_user.login).first()  
    imdbFind = ImdbFind()
    
    if 'imdb_movie_id' in request.args:
        print ("doo delete on " + request.args.get('imdb_movie_id'))
        imdbFind.deleteMovie(user, request.args.get('imdb_movie_id'))

    style = Style()
    sstyle = style.getDisplayStyle(user)
    timer.elapse('Got style')


    movies = imdbFind.displayMovies(user, request.args)  
    timer.elapse('Got movies')

    flasker = FlaskHelper()
    flasker.setArgs(user, request.args)
    form = DisplayMoviesForm()
    timer.elapse('Got DisplayMoviesForm')
    
    thisSearch = request.args.get('thisSearch')

    render = render_template('displayMovies.html', title='Display My Movies', thisSearch=thisSearch, form=form, flasker=flasker, user=user, movies=movies, sstyle=sstyle)
    timer.elapse('Got render')
    return render




@app.route('/updateMovies', methods=['GET', 'POST'])
@login_required
def updateMovies():
    print("updateMovies starts")
    style = Style()
    sstyle = style.getCommonStyle();
    message=''

    
    form = UpdateForm()
    if 'csrf_token' in request.form:
        imdbFind = ImdbFind()
        message = imdbFind.updateMovies(form.fromMovie, form.toMovie)
        
    return render_template('updateMovies.html', title='Update Movies', form=form, sstyle=sstyle, message=message)


@app.route('/inputField', methods=['GET', 'POST'])
@login_required
def inputField():
    inputter = Inputter()
    message = inputter.processInput(request.form['imdbMovieId'],
                          request.form['name'],
                          request.form['value'],
                          request.form['dataType'])
    
    return message

@app.route('/inputSettingsDisplayField', methods=['GET', 'POST'])
@login_required
def inputSettingsDisplayField():
    print ('inputSettingsDisplayField called')
    print(request.form)
    
    user = User.query.filter_by(login = current_user.login).first()  
    inputter = Inputter()
    message = inputter.processSettingsDisplayInput(user, 
                        request.form['name'],
                        request.form['colAttribute'],
                        request.form['dataType'],
                        request.form['value'])
    print("message=" + message)
    return message



@app.route('/settings')
@login_required
def settings():
    style = Style()
    sstyle = style.getCommonStyle();
    
    flasker = FlaskHelper()
        
    return render_template('settings.html', title='Settings', sstyle=sstyle, flasker=flasker, settings='none')

@app.route('/settings_account', methods=['GET', 'POST'])
@login_required
def settings_account():

        
    style = Style()
    sstyle = style.getCommonStyle();
    user = User.query.filter_by(login = current_user.login).first()
    
    flasker = FlaskHelper()
    flasker.setArgs(user, None)
    form = SettingsAccountForm()

    if form.validate_on_submit():
        flasker.updateUser(form)
        flash('Your account settings have been changed.')
                
    else:
        form.firstName.data = user.firstName
        form.lastName.data = user.lastName
        form.login.data = user.login
        form.email.data = user.email
        form.password.data = 'NothingToSee'
        form.password2.data = 'NothingToSee'
        
        print('form.password.data=' + form.password.data)
    return render_template('settings.html', title='Account Settings', sstyle=sstyle, flasker=flasker, form=form, settings='account')

@app.route('/settings_display')
@login_required
def settings_display():
    style = Style()
    sstyle = style.getCommonStyle();
    
    user = User.query.filter_by(login = current_user.login).first()  
    flasker = FlaskHelper()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle,  flasker=flasker, user=user, settings='display')


@app.route('/settings_display_upCol')
@login_required
def settings_display_upCol():
    print("in Route settings_display_upCol")
    print(request.args)
    style = Style()
    sstyle = style.getCommonStyle();
    
    selectCol = request.args.get('name')
    user = User.query.filter_by(login = current_user.login).first()  
    flasker = FlaskHelper()
    flasker.setArgs(user, None)
    flasker.upCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle,  flasker=flasker, user=user, settings='display', selectCol=selectCol)

@app.route('/settings_display_dnCol')
@login_required
def settings_display_dnCol():
    style = Style()
    sstyle = style.getCommonStyle();
    
    selectCol = request.args.get('name')
    user = User.query.filter_by(login = current_user.login).first()  
    flasker = FlaskHelper()
    flasker.setArgs(user, None)
    flasker.dnCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle,  flasker=flasker, user=user, settings='display', selectCol=selectCol)


@app.route('/settings_display_resetCol')
@login_required
def settings_display_resetCol():

    style = Style()
    sstyle = style.getCommonStyle();
    
    selectCol = request.args.get('name')
    print('settings_display_resetCol starts, name=' + selectCol)
    
    
    user = User.query.filter_by(login = current_user.login).first()  
    flasker = FlaskHelper()
    flasker.setArgs(user, None)
    flasker.resetCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle,  flasker=flasker, user=user, settings='display', selectCol=selectCol)

@app.route('/settings_display_resetSort')
@login_required
def settings_display_resetSort():

    style = Style()
    sstyle = style.getCommonStyle();
    
    selectCol = ""
    
    user = User.query.filter_by(login = current_user.login).first()  
    flasker = FlaskHelper()
    flasker.setArgs(user, None)
    flasker.resetSort()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle,  flasker=flasker, user=user, settings='display', selectCol=selectCol)


@app.route('/settings_display_resetAll')
@login_required
def settings_display_resetAll():

    style = Style()
    sstyle = style.getCommonStyle();
    
    selectCol = ""
    
    user = User.query.filter_by(login = current_user.login).first()  
    flasker = FlaskHelper()
    flasker.setArgs(user, None)
    flasker.resetAll()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle,  flasker=flasker, user=user, settings='display', selectCol=selectCol)

@app.route('/test')
@login_required
def test():
    return render_template('test.html')

@app.template_filter()
def formatter(value, fmt):
    if value == None:
        rtn = ""
    elif fmt == 'int':
        if value == 0:
            rtn = ""
        else:
            rtn = value
    elif fmt == 'date':
        rtn = '{d.month}/{d.day}/{d.year}'.format(d=value)
    elif fmt == "time":
        rtn = str(value)[1:5]
    elif fmt == "comma":
        rtn = "{:,.0f}".format(float(value))
    return rtn



