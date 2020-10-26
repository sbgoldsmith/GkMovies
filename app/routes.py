from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, SettingsAccountForm, ResetPasswordRequestForm, ResetPasswordChangeForm, UpdateByOldestForm, UpdateSingleForm, AsUserForm, ContactForm, AdminDeleteUserForm
from app.models import User
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.urls import url_parse
from Library.StyleModuleF import Style
from Library.AdderModuleF import Adder
from Library.FlaskModule import Flasker
from Library.ModelModule import UserManager
from Library.ServerModule import Inputter
from Library.PagerModule import Pager
from Library.SearchModule import Searcher
from Library.ContactModule import Contacter
from Library.LoggerModule import info, debug, Timer
from Library.VersionModule import getLatestVersion, getAllVersions, getNewVersions
from Library.UpdateReleaseModule import UpdateRelease
from Library.OmdbModule import Omdb
from Library.RapidModule import Rapid
from Library.DisplayModule import Display
from Library.SessionModule import Sessioner
from Library.AdminModule import Adminer
from datetime import datetime, timedelta
from app.email import send_password_reset_email
import random
from dominate.tags import form
import jsonpickle


version = '1.4.0'
titles = {'home':'Home Page', 'addMovies':'Add to My Movies', 'displayMovies':'Display My Movies', 'settings':'Settings', 'contact':'Contact Us'}
common = Style().getCommonStyle()

def init(defName):
          
    if current_user and current_user.is_authenticated:
        current_user.log(defName, 'init', '')


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
            
        return render_template('index.html', title='Welcome to Goldkeys Movies', sstyle=common, form=form)
    
    
    user = User.query.filter_by(login=form.login.data).first()
    if user is None or not user.check_password(form.password.data):
        info("Invalid user or password")
        flash('Sorry, the login / password combination was not recognized')

        return render_template('index.html', title='Welcome to Goldkeys Movies', sstyle=common, form=form)
    
  
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
    
    return render_template('home.html', title='Home Page', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, version=version, newVersions=newVersions, rand=rand())


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
        um = UserManager()
        user = um.addUser(form)
        um.addUserColumns(user)
        db.session.commit()
        
        info('Registered new user  ' + user.login)
        user.log('register', 'success', '')
        flash('Congratulations, you are now a registered user! Please login.')
        
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', sstyle=common, form=form)

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
    return render_template('reset_password_request.html', title='Request Password Reset', sstyle=common, form=form)
    
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
    
    return render_template('reset_password_change.html', title='Reset Your Password', sstyle=common, form=form)

    
@app.route('/addMovies', methods=['GET', 'POST'])
@login_required
def addMovies():
    info()
    init('addMovies')

    omdb = Omdb()
    rapid = Rapid()
    
    movies = []
    persons = []
    genres = rapid.getGenreList()
    
    flasker = Flasker()
    
    sess = Sessioner(version)
    searcher = sess.get('searcher')   
    searcher.setArgs(request.args)      
    sess.put('searcher', searcher)
    
    action = request.args.get('action', '')
    genreCode = request.args.get('genreCode', '')
    
    typeSelect = searcher.addTypeSelect
    addTitleSearch = searcher.addTitle
    addPersonSearch = searcher.addPerson
    addLesserSearch = searcher.addLesser
    
    if action == 'titleSearchOmdb':
        #
        # Return a list of movies for a given title
        #

        current_user.log('addMovies', 'titleSearchOmdb', addTitleSearch)
        movies = omdb.find(current_user, addTitleSearch)
        
    elif action == 'titleSearchRapid':
        current_user.log('addMovies', 'titleSearchRapid', addTitleSearch)
        movies = rapid.listMovies(current_user, addTitleSearch)
        
    elif action == 'personListRapid':
        #
        # Return a list of movies for a given nm
        #
        nm = request.args.get('nameId')
        info('Listing movies for nm=' + nm)
        persons = rapid.listPerson(nm)
        movies = rapid.listPersonMovies(current_user, nm)
        

    elif action == 'personSearchRapid':
        #
        # Return a list of persons for a given name
        #
        current_user.log('addMovies', 'personSearchRapid', addPersonSearch)
        persons = rapid.listPersons(addPersonSearch, addLesserSearch)

    elif action == 'popularListGenreRapid':
        #
        # Return a list of persons for a given name
        #
        genreCode = request.args.get('genreCode', '')
        current_user.log('addMovies', 'popularListGenreRapid', genreCode)
        movies = rapid.listMoviesByGenre(current_user, genreCode)

    return render_template('addMovies.html', title='Add to My Movies', sstyle=Style().getAdderStyle(), form=form, user=current_user, flasker=flasker, addTitleSearch=addTitleSearch, addPersonSearch=addPersonSearch, addLesserSearch=addLesserSearch,  omdb=omdb, typeSelect=typeSelect, genreCode=genreCode, persons=persons, genres=genres, movies=movies)

@app.route('/addMovie', methods=['GET', 'POST'])
@login_required
def addMovie():
    tt = request.form['tt']
    displayType = request.form['displayType']
    
    info('addMovie, tt=' + tt + ', displayType=' + displayType)
    init('addMovie')
    
    current_user.log('addMovie', 'tt, displayType', tt + "," + displayType)
    adder = Adder()
    response = adder.addMovie(current_user, tt, displayType)
    json = jsonpickle.encode(response)

    return json

@app.route('/addImdb', methods=['GET', 'POST'])
@login_required
def addImdb():
    info()
    init('addImdb')
    current_user.log('addImdb', 'tt', request.form['tt'])
    adder = Adder()
    message = adder.addImdb(request.form['tt'])
    
    return message

@app.route('/refreshAdder', methods=['GET', 'POST'])
@login_required
def refreshAdder():
    tt = request.form['tt']
    what = request.form['what']
    info('tt=' + tt + ', what=' + what)
    init('refreshAdder')
    rapid = Rapid()
    message = rapid.refreshAdder(tt, what)
    return message

@app.route('/displayMovies', methods=['GET', 'POST'])
@login_required
def displayMovies():

    info()
    init('displayMovies')

    timer = Timer()
    display = Display()
    
    if 'imdb_movie_id' in request.args:
        current_user.log('displayMovies', 'delete', request.args.get('imdb_movie_id'))
        display.deleteMovie(current_user, request.args.get('imdb_movie_id'))

    
    sess = Sessioner(version)
    searcher = sess.get('searcher')   
    searcher.setArgs(request.args)      

    style = Style()
    sstyle = style.getDisplayStyle(current_user, searcher.displayType)
    
    sortButton = request.args.get('sortButton')
    
    movies = display.displayMovies(current_user, searcher, sortButton)
    timer.elapse('Got movies')
    
    #Saving searcher here because display.displayMovies might have changed it.
    sess.put('searcher', searcher)
    

    pager = sess.get('pager')   
    pager.setArgs(request.args, searcher, len(movies))    
    sess.put('pager', pager)
    
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    #form = DisplayMoviesForm() form=form, 
    
        
    #logArg = str(thisSearch) + '=' + str(request.args.get(thisSearch)) + ' order ' + str(request.args.get('sortButton'))
    #current_user.log('displayMovies', 'thisSearch',  logArg)
    
    thisSearch = searcher.getThis() + 'Search'
    render = render_template('displayMovies.html', title='Display My Movies', sstyle=sstyle, user=current_user, flasker=flasker, pager=pager, searcher=searcher, thisSearch=thisSearch, movies=movies, title_line = 'displayMoviesButtons.html')

    timer.elapse('Got render')
    return render

@app.route('/movie_seen', methods=['GET', 'POST'])
@login_required
def movie_seen():
    tt = request.args['tt']
    
    info(tt)
    init('movie_seen, tt=' + tt)
    display = Display()
    display.seen(current_user, tt)
    
    return displayMovies()

@app.route('/inputField', methods=['GET', 'POST'])
@login_required
def inputField():
    init('inputField')
    inputter = Inputter()
    message = inputter.processInput(request.form['imdbMovieId'],
                          request.form['name'],
                          request.form['value'],
                          request.form['dataFormat'])
    
    return message

@app.route('/inputSettingsDisplayField', methods=['GET', 'POST'])
@login_required
def inputSettingsDisplayField():
    init('inputSettingsDisplayField') 
    inputter = Inputter()
    message = inputter.processSettingsDisplayInput(current_user, 
                        request.form['name'],
                        request.form['displayType'],
                        request.form['colAttribute'],
                        request.form['dataFormat'],
                        request.form['value'])

    return message


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    init('settings') 
    sess = Sessioner(version)
    if not sess.get('settings') or not sess.get('settings-expire'):
        sess.put('settings', 'none')
        sess.put('settings-expire', datetime.now() + timedelta(hours=1))
                  
    if datetime.now() > sess.get('settings-expire'):
        sess.put('settings', 'none')

    info('settings, skey=' + sess.get('settings'))
    
    if sess.get('settings') == 'account':
        return settings_account()
    elif sess.get('settings') == 'display':
        return settings_display()
    elif sess.get('settings') == 'reset':
        return settings_reset()
    else:
        current_user.log('settings', '', '')
        flasker = Flasker()
        
        return render_template('settings.html', title='Settings', sstyle=common, flasker=flasker, settings='none')
       
@app.route('/settings_account', methods=['GET', 'POST'])
@login_required
def settings_account():
    init('settings_account') 
    
    sess = Sessioner(version)
    sess.put('settings', 'account')
    sess.put('settings-expire', datetime.now() + timedelta(hours=1))
    
    info('settings, skey=' + sess.get('settings'))
    flasker = Flasker()
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
        form.city.data = current_user.city
        form.stateSelect.data = current_user.state
        form.countrySelect.data = current_user.country
        form.password.data = 'NothingToSee'
        form.password2.data = 'NothingToSee'
        

    return render_template('settings.html', title='Account Settings', sstyle=common, form=form, user=current_user, flasker=flasker, settings='account')

@app.route('/settings_display')
@login_required
def settings_display():
    init('settings_display') 
    sess = Sessioner(version)
    sess.put('settings', 'display')
    sess.put('settings-expire', datetime.now() + timedelta(hours=1))

    info('settings, skey=' + sess.get('settings'))
    current_user.log('settings', 'display', '')
    flasker = Flasker()
    
    searcher = sess.get('searcher')
    searcher.setArgs(request.args)  
    sess.put('searcher', searcher)
    
    
    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, searcher=searcher, settings='display')


@app.route('/settings_display_upCol')
@login_required
def settings_display_upCol():
    info()
    init('settings_display_upCol') 
    selectCol = request.args.get('name')
    
    sess = Sessioner(version)
    searcher = sess.getWithArgs('searcher', request.args)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.upCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, settings='display', searcher=searcher, selectCol=selectCol)

@app.route('/settings_display_dnCol')
@login_required
def settings_display_dnCol():
    info()
    init('settings_display_dnCol') 
    selectCol = request.args.get('name')

    sess = Sessioner(version)
    searcher = sess.getWithArgs('searcher', request.args)

    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.dnCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, settings='display', searcher=searcher, selectCol=selectCol)


@app.route('/settings_display_resetCol')
@login_required
def settings_display_resetCol():
    info()  
    init('settings_display_resetCol')    
    selectCol = request.args.get('name')
    
    sess = Sessioner(version)
    searcher = sess.getWithArgs('searcher', request.args)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.resetCol(selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, settings='display', searcher=searcher, selectCol=selectCol)

@app.route('/settings_display_resetSort')
@login_required
def settings_display_resetSort():
    info()  
    init('settings_display_resetSort')   
    selectCol = ""
     
    sess = Sessioner(version)
    searcher = sess.getWithArgs('searcher', request.args)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.resetSort()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common,  user=current_user,  flasker=flasker, settings='display', searcher=searcher, selectCol=selectCol)


@app.route('/settings_display_resetAll')
@login_required
def settings_display_resetAll():
    info()    
    init('settings_display_resetAll')    
    selectCol = ""
         
    sess = Sessioner(version)
    searcher = sess.getWithArgs('searcher', request.args)

    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.resetAll()
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common,  user=current_user,  flasker=flasker, settings='display', searcher=searcher, selectCol=selectCol)


@app.route('/settings_reset')
@login_required
def settings_reset():
    init('settings_reset') 
    sess = Sessioner(version)
    sess.put('settings', 'reset')
    sess.put('settings-expire', datetime.now() + timedelta(hours=1))
   
    
    info('settings, skey=' + sess.get('settings'))
    current_user.log('settings', 'reset', '')
    flasker = Flasker()
    
        
    reset = request.args.get('reset')
    if reset == 'pager' or reset == 'all':
        current_user.log('settings', 'reset', 'pager')
        sess.put('pager', Pager())
        flash('Paging session reset')
        
    if reset == 'searcher' or reset == 'all': 
        current_user.log('settings', 'reset', 'searcher')
        sess.put('searcher', Searcher())
        flash('Searching session reset')
        
    if reset == 'all': 
        sess.put('settings-expire', datetime.now())
        flash('Misc other session reset')
        
    return render_template('settings.html', title='Reset Settings', sstyle=common, user=current_user, flasker=flasker, settings='reset')


@app.route('/updateMovies', methods=['GET', 'POST'])
@login_required
def updateMovies():
    info()  
    init('updateMovies')   
   
    current_user.log('updateMovies', '', '')
    
    adder = Adder()
    oldestForm = UpdateByOldestForm()
    singleForm = UpdateSingleForm()
    
    oldest_message = ''
    single_message = ''
    
    if 'csrf_token' in request.form:
       
        if request.form.get('submit') == oldestForm.submit.label.text:
            #
            # Oldest Update of Movies
            #
            info('oldestForm = ' + str(oldestForm.cnt.data))
            current_user.log('updateMovies', 'oldest', str(oldestForm.cnt.data))
            oldest_message = adder.updateOldestImdbMovies(oldestForm.cnt.data, oldestForm.oldestGenres.data, oldestForm.oldestCast.data)
        
        elif request.form.get('submit') == singleForm.submit.label.text:
            #
            # Single Movie
            #
            info('tt = ' + str(singleForm.tt.data))
            single_message = adder.updateSingleImdbMovie(singleForm.tt.data, singleForm.singleGenres.data, singleForm.singleCast.data)
        
        else:
            oldest_message = 'Error: unrecognized submit = ' + str(request.args.get('submit'))
            
    return render_template('updateMovies.html', title='Update Movies', sstyle=common, oldestForm=oldestForm, singleForm=singleForm, oldest_message=oldest_message, single_message=single_message)



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
        contacter.send_contact_email()

        sent = True
                    
        if current_user.is_authenticated:
            current_user.log('contact', 'success', '')

    return render_template('contact.html', title='Contact Us', user=current_user, flasker=Flasker(), sstyle=common, form=form, sent=sent)



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
            
    return render_template('asUser.html', title='Login As User', flasker=Flasker(), sstyle=common, form=form, message=message)
 

@app.route('/adminDeleteUser', methods=['GET', 'POST'])
@login_required
def adminDeleteUser():
    info()     

    message = []
    form = AdminDeleteUserForm()
    
    if 'csrf_token' in request.form:
        
        adminer = Adminer()
        message = adminer.deleteUser(form.userSelect.data)
            
    return render_template('admin_delete_user.html', title='Delete a User', flasker=Flasker(), sstyle=common, form=form, message=message)
 


@app.route('/help', methods=['GET', 'POST'])
@login_required
def help():
    info() 
    current_user.log('help', request.args.get('path'), '')
    imagePath = 'images/help/' + request.args.get('path') + '.png'
    includePath = 'helpInclude/' + request.args.get('path') + '.html'
    title = titles[request.args.get('path')]

    return render_template('help.html', title=title, style=Style().getHelpStyle(), imagePath=imagePath, includePath=includePath, rand=rand())


@app.route('/versions')
@login_required
def versions():
    info()
    init('versions')
    versions = getAllVersions()

    return render_template('versions_all.html', title='Release Notes', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, versions=versions)


@app.route('/versions_new')
@login_required
def versions_new():
    info()
    init('versions_new')
    versions_new = getNewVersions()
    current_user.setLastVisit()
    return render_template('versions_new.html', title='Release Notes', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, versions=versions_new, rand=rand())
 

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

    return render_template('admin.html', title='Administration Functions', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user)
 
 
@app.route('/updateRelease', methods=['GET', 'POST'])
@login_required
def updateRelease():
    info()
    init('updateRelease')
    
    message = ''

    if 'step' in request.args:
        version = request.args['version']
        step = request.args['step']
        us = UpdateRelease()
        message = us.update(version, step)
        info('message = ' + message)
    return render_template('updateRelease.html', title='Update Release', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, form=form, message=message)
 
 
 
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


