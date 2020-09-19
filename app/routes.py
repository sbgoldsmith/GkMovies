from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, SettingsAccountForm, ResetPasswordRequestForm, ResetPasswordChangeForm, AddMoviesForm, DisplayMoviesForm, UpdateRangeForm, UpdateSingleForm, AsUserForm, ContactForm, UpdateSchemaForm
from app.models import User, AdderColumn
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.urls import url_parse
from app.Imdb import ImdbFind
from Library.StyleModuleF import Style
from Library.AdderModuleF import Adder
from Library.FlaskModule import FlaskHelper
from Library.ModelModule import addUserColumns
from Library.ServerModule import Inputter
from Library.PagerModule import Pager
from Library.SearchModule import Searcher
from Library.ContactModule import Contacter
from Library.LoggerModule import info, debug, Timer
from Library.VersionModule import getLatestVersion, getAllVersions, getNewVersions
from Library.UpdateSchemaModule import UpdateSchema
from datetime import datetime, timedelta
from app.Imdb import ImdbFind
from app.email import send_password_reset_email
import jsonpickle
import random

version = '1.3'
titles = {'home':'Home Page', 'addMovies':'Add to My Movies', 'displayMovies':'Display My Movies', 'settings':'Settings', 'contact':'Contact Us'}

def skey(key):
    if hasattr(current_user, 'id'):
        return key + '_' + str(current_user.id)
    else:
        return key
    
def initJsonSession(name, obj):  
    if skey(name) not in session or session[skey('version')] != version:
        debug('Initialize Json session ' + skey(name))
        session[skey(name)] = jsonpickle.encode(obj)
 
def initSimpSession(name, obj):       
    if skey(name) not in session or session[skey('version')] != version:   
        debug('Initialize Simp session ' + skey(name))
        session[skey(name)] = obj
        
        
def init(defName):
    #info(defName + ' init')


    initJsonSession('pager', Pager())        
    initJsonSession('searcher', Searcher())  
    initSimpSession('sstyle', Style().getCommonStyle())
    initSimpSession('version', version)
        
    if current_user and current_user.is_authenticated:
        current_user.log(defName, 'init', '')

        
def sstyle():
    return session[skey('sstyle')]

def rand():
    return random.randint(1, 999999)

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
            
        return render_template('index.html', title='Welcome to Goldkeys Movies', sstyle=sstyle(), form=form)
    
    
    user = User.query.filter_by(login=form.login.data).first()
    if user is None or not user.check_password(form.password.data):
        info("Invalid user or password")
        flash('Sorry, the login / password combination was not recognized')

        return render_template('index.html', title='Welcome to Goldkeys Movies', sstyle=sstyle(), form=form)
    
  
    login_user(user)
    
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')

    return redirect(url_for('home'))
   

@app.route('/home')
@login_required
def home():
    info('Browser=' + request.user_agent.browser + ' on ' + request.user_agent.platform)
    init('home')
    
    version = getLatestVersion()
    newVersions = getNewVersions()
    
    if len(newVersions) == 0:
        current_user.setLastVisit()
    
    return render_template('home.html', title='Home Page', sstyle=Style().getHomeStyle(), user=current_user, version=version, newVersions=newVersions)


@app.route('/logout')
def logout():
    init('logout')
    current_user.logout()
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
                    as_login = form.login.data, 
                    user_since = datetime.utcnow(),
                    last_visit = datetime.utcnow())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        

        addUserColumns(user)
        info('Registered new user  ' + user.login)
        user.log('register', 'success', '')
        flash('Congratulations, you are now a registered user! Please login.')
        
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', sstyle=sstyle(), form=form)

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
    return render_template('reset_password_request.html', title='Request Password Reset', sstyle=sstyle(), form=form)
    
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
    
    return render_template('reset_password_change.html', title='Reset Your Password', sstyle=sstyle(), form=form)

    
@app.route('/addMovies', methods=['GET', 'POST'])
@login_required
def addMovies():
    info()
    init('addMovies')
    if request.args.get('titleSearch') == None:
        titleSearch = ""
    else:
        titleSearch = str(request.args.get('titleSearch'))
        
        
        
    current_user.log('addMovies', 'titleSearch', titleSearch)
    imdbFind = ImdbFind()
    movies = imdbFind.findMovies(current_user, titleSearch)
    
    status = ""
    if len(movies) == 0 and len(titleSearch) > 0:
        status = "No results yet.  Try entering more characters."

    form = AddMoviesForm()
    return render_template('addMovies.html', title='Add to My Movies', sstyle=Style().getAdderStyle(), form=form, user=current_user, imdbFind=imdbFind, titleSearch=titleSearch, movies=movies, status=status)

@app.route('/addMovie', methods=['GET', 'POST'])
@login_required
def addMovie():
    info()
    init('addMovie')
    current_user.log('addMovie', 'tt', request.form['tt'])
    adder = Adder()
    message = adder.addMovie(request.form['tt'])
    
    return message

@app.route('/addImdb', methods=['GET', 'POST'])
@login_required
def addImdb():
    info()
    init('addImdb')
    current_user.log('addImdb', 'tt', request.form['tt'])
    adder = Adder()
    message = adder.addImdb(request.form['tt'])
    
    return message



@app.route('/displayMovies', methods=['GET', 'POST'])
@login_required
def displayMovies():
    info()
    init('displayMovies')

    timer = Timer()
    imdbFind = ImdbFind()
    
    if 'imdb_movie_id' in request.args:
        current_user.log('displayMovies', 'delete', request.args.get('imdb_movie_id'))
        imdbFind.deleteMovie(current_user, request.args.get('imdb_movie_id'))
    
    
    style = Style()
    sstyle = style.getDisplayStyle(current_user)

    searcher = jsonpickle.decode(session[skey('searcher')]) 
    searcher.setArgs(request.args)      

    
    sortButton = request.args.get('sortButton')
    
    movies = imdbFind.displayMovies(current_user, searcher, sortButton)
    timer.elapse('Got movies')
    #Saving searcher here because Imdb might have changed it.
    session[skey('searcher')] = jsonpickle.encode(searcher)
    

    pager = jsonpickle.decode(session[skey('pager')]) 
    pager.setArgs(request.args, searcher, len(movies))    
    session[skey('pager')] = jsonpickle.encode(pager)
    
    
    flasker = FlaskHelper()
    flasker.setArgs(current_user, searcher)
    form = DisplayMoviesForm()
    
        
    #logArg = str(thisSearch) + '=' + str(request.args.get(thisSearch)) + ' order ' + str(request.args.get('sortButton'))
    #current_user.log('displayMovies', 'thisSearch',  logArg)
    
    thisSearch = searcher.this + 'Search'
    render = render_template('displayMovies.html', title='Display My Movies', sstyle=sstyle, form=form, user=current_user, flasker=flasker, pager=pager, searcher=searcher, thisSearch=thisSearch, movies=movies)

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
    if skey('settings') not in session or skey('settings-expire') not in session:
        session[skey('settings')] = 'none'
        session[skey('settings-expire')] = datetime.now() - timedelta(hours=1)
                  
    if datetime.now() > session[skey('settings-expire')]:
        session[skey('settings')] = 'none'

    info('settings, skey=' + skey('settings'))
    
    if session[skey('settings')] == 'account':
        return settings_account()
    elif session[skey('settings')] == 'display':
        return settings_display()
    elif session[skey('settings')] == 'reset':
        return settings_reset()
    else:
        current_user.log('settings', '', '')
        flasker = FlaskHelper()
        
        return render_template('settings.html', title='Settings', sstyle=sstyle(), flasker=flasker, settings='none')
       
@app.route('/settings_account', methods=['GET', 'POST'])
@login_required
def settings_account():
    init('settings_account') 
    session[skey('settings')] = 'account'
    session[skey('settings-expire')] = datetime.now() + timedelta(hours=1)
    
    info('settings, skey=' + skey('settings'))
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    form = SettingsAccountForm()

    if form.validate_on_submit():
        info('Settings account submitted')
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
        
    return render_template('settings.html', title='Account Settings', sstyle=sstyle(), form=form, flasker=flasker, settings='account')

@app.route('/settings_display')
@login_required
def settings_display():
    init('settings_display') 
    session[skey('settings')] = 'display'
    session[skey('settings-expire')] = datetime.now() + timedelta(hours=1)
    
    info('settings, skey=' + skey('settings'))
    current_user.log('settings', 'display', '')
    flasker = FlaskHelper()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle(), user=current_user, flasker=flasker, settings='display')


@app.route('/settings_reset')
@login_required
def settings_reset():
    init('settings_reset') 
    session[skey('settings')] = 'reset'
    session[skey('settings-expire')] = datetime.now() + timedelta(hours=1)
    
    info('settings, skey=' + skey('settings'))
    current_user.log('settings', 'reset', '')
    flasker = FlaskHelper()
    
        
    sess = request.args.get('sess')
    if sess == 'pager' or sess == 'all':
        current_user.log('settings', 'reset', 'pager')
        session[skey('pager')] = jsonpickle.encode(Pager())
        flash('Paging session reset')
        
    if sess == 'searcher' or sess == 'all': 
        current_user.log('settings', 'reset', 'searcher')
        session[skey('searcher')] = jsonpickle.encode(Searcher())
        flash('Searching session reset')
        
    if sess == 'all': 
        session[skey('settings-expire')] = datetime.now()
        flash('Misc other session reset')
        
    return render_template('settings.html', title='Reset Settings', sstyle=sstyle(), user=current_user, flasker=flasker, settings='reset')


@app.route('/settings_display_upCol')
@login_required
def settings_display_upCol():
    info()
    init('settings_display_upCol') 
    selectCol = request.args.get('name')

    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.upCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle(), user=current_user, flasker=flasker, settings='display', selectCol=selectCol)

@app.route('/settings_display_dnCol')
@login_required
def settings_display_dnCol():
    info()
    init('settings_display_dnCol') 
    selectCol = request.args.get('name')

    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.dnCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle(), user=current_user, flasker=flasker, settings='display', selectCol=selectCol)


@app.route('/settings_display_resetCol')
@login_required
def settings_display_resetCol():
    info()  
    init('settings_display_resetCol')    
    selectCol = request.args.get('name')
    
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.resetCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle(), user=current_user, flasker=flasker, settings='display', selectCol=selectCol)

@app.route('/settings_display_resetSort')
@login_required
def settings_display_resetSort():
    info()  
    init('settings_display_resetSort')   
    selectCol = ""
     
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.resetSort()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle(),  user=current_user,  flasker=flasker, settings='display', selectCol=selectCol)


@app.route('/settings_display_resetAll')
@login_required
def settings_display_resetAll():
    info()    
    init('settings_display_resetAll')    
    selectCol = ""
    
    flasker = FlaskHelper()
    flasker.setArgs(current_user, None)
    flasker.resetAll()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=sstyle(),  user=current_user,  flasker=flasker, settings='display', selectCol=selectCol)


@app.route('/updateMovies', methods=['GET', 'POST'])
@login_required
def updateMovies():
    info()  
    init('updateMovies')   
   
    current_user.log('updateMovies', '', '')
    
    imdbFind = ImdbFind()
    rangeForm = UpdateRangeForm()
    singleForm = UpdateSingleForm()
    
    range_message = ''
    single_message = ''
    
    if 'csrf_token' in request.form:
       
        if request.form.get('submit') == rangeForm.submit.label.text:
            info('range = ' + str(rangeForm.fromMovie.data) + " > " + str(rangeForm.toMovie.data))
            current_user.log('updateMovies', 'range', str(rangeForm.fromMovie.data) + " > " + str(rangeForm.toMovie.data))
            range_message = imdbFind.updateMovies(rangeForm.fromMovie, rangeForm.toMovie, rangeForm.rangeGenres.data, rangeForm.rangeCast.data)
        
        elif request.form.get('submit') == singleForm.submit.label.text:
            info('tt = ' + str(singleForm.tt.data))
            imovie = imdbFind.updateMovie(singleForm.tt.data, singleForm.singleGenres.data, singleForm.singleCast.data)
            single_message = "Updated '" + imovie.title + "'"
        
        else:
            range_message = 'Error: unrecognized submit = ' + str(request.args.get('submit'))
            
    return render_template('updateMovies.html', title='Update Movies', sstyle=sstyle(), rangeForm=rangeForm, singleForm=singleForm, range_message=range_message, single_message=single_message)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    info()  
    init('contact')   
    form = ContactForm()
    
    sent = False
    
    if 'csrf_token' in request.form and current_user.is_authenticated:
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.email.data = current_user.email
        
    if form.validate_on_submit():
        info('Contact Us Submitted, subject=' + form.subject.data)
 
        contacter = Contacter(current_user, form)
        contacter.addContact()
        contacter.sendEmail()
        sent = True
                    
        if current_user.is_authenticated:
            current_user.log('contact', 'success', '')

    return render_template('contact.html', title='Contact Us', user=current_user, sstyle=sstyle(), form=form, sent=sent)



@app.route('/asUser', methods=['GET', 'POST'])
@login_required
def asUser():
    info()     

    message = ''
    form = AsUserForm()
    if 'csrf_token' in request.form:
        user = User.query.filter_by(login=form.login.data).first()
        if user is None:
            current_user.log('asUser', 'login fail', form.login.data)
            message = "login '" + form.login.data + "' is not a valid login"
        else:
            orig = current_user.login
            info("Login As User " + form.login.data)
            current_user.log('asUser', 'login success', form.login.data)
            message = "You are now logged in as '" + form.login.data + "'"
            login_user(user)
            current_user.asLogin(orig)
            init('asUser')
            
    return render_template('asUser.html', title='Login As User', sstyle=sstyle(), form=form, message=message)
 

@app.route('/help', methods=['GET', 'POST'])
@login_required
def help():
    info() 
    current_user.log('help', request.args.get('path'), '')
    imagePath = 'images/help/' + request.args.get('path') + '.png'
    includePath = 'helpInclude/' + request.args.get('path') + '.html'
    title = titles[request.args.get('path')]

    return render_template('help.html', title=title, imagePath=imagePath, includePath=includePath, rand=rand())


@app.route('/versions')
@login_required
def versions():
    info()
    init('versions')
    versions = getAllVersions()

    return render_template('versions_all.html', title='Release Notes', sstyle=Style().getHomeStyle(), user=current_user, versions=versions)


@app.route('/versions_new')
@login_required
def versions_new():
    info()
    init('versions_new')
    versions_new = getNewVersions()
    current_user.setLastVisit()
    return render_template('versions_new.html', title='Release Notes', sstyle=Style().getHomeStyle(), user=current_user, versions=versions_new)
 

@app.route('/lastVisit', methods=['GET', 'POST'])
@login_required
def lastVisit():
    info()
    init('lastVisit')
    current_user.setLastVisit()
    
    return ''

@app.route('/admin')
@login_required
def admin():
    info()
    init('admin')

    return render_template('admin.html', title='Administration Functions', sstyle=Style().getHomeStyle(), user=current_user)
 
 
@app.route('/updateSchema', methods=['GET', 'POST'])
@login_required
def updateSchema():
    info()
    init('updateSchema')

    message = ''
    form = UpdateSchemaForm()
    if 'csrf_token' in request.form:
        us = UpdateSchema()
        message = us.update()
        info('message = ' + message)
    return render_template('updateSchema.html', title='Update Database Schema', sstyle=Style().getHomeStyle(), user=current_user, form=form, message=message)
 
 
 
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


