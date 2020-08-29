from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, SettingsAccountForm, ResetPasswordRequestForm, ResetPasswordChangeForm, AddMoviesForm, DisplayMoviesForm, UpdateForm, AsUserForm
from app.models import User, AdderColumn
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.urls import url_parse
from app.Imdb import ImdbFind
from Library.StyleModuleF import Style
from Library.AdderModuleF import Adder
from Library.FlaskModule import FlaskHelper
from Library.TimerModule import Timer
from Library.ModelModule import addUserColumns
from Library.ServerModule import Inputter
from Library.PagerModule import Pager
from datetime import datetime, timedelta
from app.Imdb import ImdbFind
from app.email import send_password_reset_email
import logging
import jsonpickle

def info(message):
    logging.getLogger('gk').info(message)
    
    
def init(defName):
    if 'sstyle' not in session:
        style = Style()
        session['sstyle'] = style.getCommonStyle()
        
    if current_user and current_user.is_authenticated:
        current_user.log(defName, 'init', '')
        current_user.setLastVisit()
    
    info(defName + ' init')

    
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    init('index')
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()

    if not form.validate_on_submit():
        if 'csrf_token' in request.form:
            # Submit button pressed
            flash('Please enter a login and password')
            
        return render_template('index.html', title='Welcome to Goldkeys Movies', sstyle=session['sstyle'], form=form)
    
    
    user = User.query.filter_by(login=form.login.data).first()
    if user is None or not user.check_password(form.password.data):
        info("Invalid user or password")
        flash('Sorry, the login / password combination was not recognized')

        return render_template('index.html', title='Welcome to Goldkeys Movies', sstyle=session['sstyle'], form=form)
    
  
    login_user(user)
    
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')

    return redirect(url_for('home'))
   

@app.route('/home')
@login_required
def home():
    init('home')
    return render_template('home.html', title='Home Page', sstyle=Style().getHomeStyle(), user=current_user)


@app.route('/logout')
def logout():
    init('logout')
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    init('register')
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

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
        info('Registered new user  ' + user.login)
        user.log('register', 'success', '')
        flash('Congratulations, you are now a registered user! Please login.')
        
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', sstyle=session['sstyle'], form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    init('reset_password_request')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('index'))
    return render_template('reset_password_request.html', title='Request Password Reset', sstyle=session['sstyle'], form=form)
    
@app.route('/reset_password_change/<token>', methods=['GET', 'POST'])
def reset_password_change(token):   
    init('reset_password_change')
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
    
    return render_template('reset_password_change.html', title='Reset Your Password', sstyle=session['sstyle'], form=form)

    
@app.route('/addMovies', methods=['GET', 'POST'])
@login_required
def addMovies():
    init('addMovies')
    if request.args.get('titleSearch') == None:
        titleSearch = ""
    else:
        titleSearch = str(request.args.get('titleSearch'))
        
    current_user.log('addMovies', 'titleSearch', titleSearch)
    imdbFind = ImdbFind()
    movies = imdbFind.findMovies(current_user, titleSearch)

    form = AddMoviesForm()
    return render_template('addMovies.html', title='Add to My Movies', sstyle=Style().getAdderStyle(), form=form, titleSearch=titleSearch, movies=movies)

@app.route('/addMovie', methods=['GET', 'POST'])
@login_required
def addMovie():
    init('addMovie')
    current_user.log('addmovie', 'tt', request.form['tt'])
    adder = Adder()
    message = adder.addMovie(request.form['tt'])
    
    return message


@app.route('/displayMovies', methods=['GET', 'POST'])
@login_required
def displayMovies():
    init('displayMovies')
    print(request.args)
    timer = Timer()
    imdbFind = ImdbFind()
    
    if 'imdb_movie_id' in request.args:
        current_user.log('displayMovies', 'delete', request.args.get('imdb_movie_id'))
        imdbFind.deleteMovie(current_user, request.args.get('imdb_movie_id'))
    
    
    style = Style()
    sstyle = style.getDisplayStyle(current_user)
    timer.elapse('Got style')


    movies = imdbFind.displayMovies(current_user, request.args)  
    for m in range(5):
        print(movies[m].imdb_movie.title)
  
  
    timer.elapse('Got movies')

    flasker = FlaskHelper()
    flasker.setArgs(current_user, request.args)
    form = DisplayMoviesForm()
    timer.elapse('Got DisplayMoviesForm')
    
    thisSearch = request.args.get('thisSearch')
    logArg = str(thisSearch) + '=' + str(request.args.get(thisSearch)) + ' order ' + str(request.args.get('sortButton'))
            
    if 'pager' in session:
        pager = jsonpickle.decode(session['pager']) 
        
    else:
        pager = Pager()

    print('@@@@@ about to set args')
    pager.setArgs(request.args, len(movies))    
    session['pager'] = jsonpickle.encode(pager)

    
    current_user.log('displayMovies', 'thisSearch',  logArg)
    
    render = render_template('displayMovies.html', title='Display My Movies', sstyle=sstyle, form=form, user=current_user, flasker=flasker, pager=pager, thisSearch=thisSearch, movies=movies)

    timer.elapse('Got render')
    return render



@app.route('/inputField', methods=['GET', 'POST'])
@login_required
def inputField():
    init('inputField')
    inputter = Inputter()
    message = inputter.processInput(request.form['imdbMovieId'],
                          request.form['name'],
                          request.form['value'],
                          request.form['dataType'])
    
    return message

@app.route('/inputSettingsDisplayField', methods=['GET', 'POST'])
@login_required
def inputSettingsDisplayField():
    init('inputSettingsDisplayField') 
    inputter = Inputter()
    message = inputter.processSettingsDisplayInput(current_user, 
                        request.form['name'],
                        request.form['colAttribute'],
                        request.form['dataType'],
                        request.form['value'])

    return message


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    init('settings') 
    if 'settings' not in session or 'settings-expire' not in session:
        session['settings'] = 'none'
        session['settings-expire'] = datetime.now() - timedelta(minutes=1)
                  
    if datetime.now() > session['settings-expire']:
        session['settings'] = 'none'

    if session['settings'] == 'account':
        return settings_account()
    elif session['settings'] == 'display':
        return settings_display()
    else:
        current_user.log('settings', '', '')
        flasker = FlaskHelper()
        
        return render_template('settings.html', title='Settings', sstyle=session['sstyle'], flasker=flasker, settings='none')
       
@app.route('/settings_account', methods=['GET', 'POST'])
@login_required
def settings_account():
    init('settings_account') 
    session['settings'] = 'account'
    session['settings-expire'] = datetime.now() + timedelta(hours=1)
    
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    form = SettingsAccountForm()

    if form.validate_on_submit():
        current_user.log('settings', 'account', 'submit')
        flasker.updateUser(form)
        flash('Your account settings have been changed.')
                
    else:
        current_user.log('settings', 'account', 'form')
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.login.data = current_user.login
        form.email.data = current_user.email
        form.password.data = 'NothingToSee'
        form.password2.data = 'NothingToSee'
        
    return render_template('settings.html', title='Account Settings', sstyle=session['sstyle'], form=form, flasker=flasker, settings='account')

@app.route('/settings_display')
@login_required
def settings_display():
    init('settings_display') 
    session['settings'] = 'display'
    session['settings-expire'] = datetime.now() + timedelta(hours=1)
    
    current_user.log('settings', 'display', '')
    flasker = FlaskHelper()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=session['sstyle'], user=current_user, flasker=flasker, settings='display')


@app.route('/settings_display_upCol')
@login_required
def settings_display_upCol():
    init('settings_display_upCol') 
    selectCol = request.args.get('name')

    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.upCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=session['sstyle'], user=current_user, flasker=flasker, settings='display', selectCol=selectCol)

@app.route('/settings_display_dnCol')
@login_required
def settings_display_dnCol():
    init('settings_display_dnCol') 
    selectCol = request.args.get('name')

    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.dnCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=session['sstyle'], user=current_user, flasker=flasker, settings='display', selectCol=selectCol)


@app.route('/settings_display_resetCol')
@login_required
def settings_display_resetCol():
    init('settings_display_resetCol')    
    selectCol = request.args.get('name')
    
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.resetCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=session['sstyle'], user=current_user, flasker=flasker, settings='display', selectCol=selectCol)

@app.route('/settings_display_resetSort')
@login_required
def settings_display_resetSort():
    init('settings_display_resetSort')   
    selectCol = ""
     
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.resetSort()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=session['sstyle'],  user=current_user,  flasker=flasker, settings='display', selectCol=selectCol)


@app.route('/settings_display_resetAll')
@login_required
def settings_display_resetAll():  
    init('settings_display_resetAll')    
    selectCol = ""
    
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.resetAll()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=session['sstyle'],  user=current_user,  flasker=flasker, settings='display', selectCol=selectCol)


@app.route('/updateMovies', methods=['GET', 'POST'])
@login_required
def updateMovies():
    init('updateMovies')   
    message=''
    current_user.log('updateMovies', '', '')
    
    form = UpdateForm()
    if 'csrf_token' in request.form:
        info('Update Movies, range = ' + str(form.fromMovie.data) + " > " + str(form.toMovie.data))
        current_user.log('updateMovies', 'range', str(form.fromMovie.data) + " > " + str(form.toMovie.data))
        imdbFind = ImdbFind()
        message = imdbFind.updateMovies(form.fromMovie, form.toMovie)
        
    return render_template('updateMovies.html', title='Update Movies', sstyle=session['sstyle'], form=form, message=message)


@app.route('/asUser', methods=['GET', 'POST'])
@login_required
def asUser():
    init('asUser') 
    message = ''
    form = AsUserForm()
    if 'csrf_token' in request.form:
        user = User.query.filter_by(login=form.login.data).first()
        if user is None:
            current_user.log('asUser', 'login fail', form.login.data)
            message = "login '" + form.login.data + "' is not a valid login"
        else:
            info("Login As User " + form.login.data)
            current_user.log('asUser', 'login success', form.login.data)
            message = "You are now logged in as '" + form.login.data + "'"
            login_user(user)
        
    return render_template('asUser.html', title='Login As User', sstyle=session['sstyle'], form=form, message=message)


@app.route('/reset_session')
@login_required
def reset_session():
    init('reset_session')
    pager = Pager()
    session['pager'] = jsonpickle.encode(pager)


    return render_template('home.html', title='Home Page', sstyle=session['sstyle'], user=current_user)



@app.route('/test')
@login_required
def test():
    return render_template('test.html')

@app.template_filter()
def formatter(value, fmt):
    if value == None:
        rtn = ""
    elif fmt == 'date':
        if value == '0000-00-00':
            rtn = ''
        else:
            rtn = '{d.month}/{d.day}/{d.year}'.format(d=value)
    elif fmt == "time":
        rtn = str(value)[1:5]
    elif fmt == "comma":
        steve = 1
        rtn = "{:,.0f}".format(float(value))
    return rtn


