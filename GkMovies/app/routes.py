from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, SettingsAccountForm, ResetPasswordRequestForm, ResetPasswordChangeForm
from app.forms import UpdateByOldestForm, UpdateSingleForm, UpdateRankForm, AsUserForm, ContactForm, AdminDeleteUserForm
from app.forms import RankListForm, RankShowMineForm, GenreCheckBoxesForm, ClubCreateForm, ClubManageForm, ClubSearchForm
from app.models import User
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.urls import url_parse
from Library.StyleModuleF import Style
from Library.AdderModuleF import Adder
from Library.FlaskModule import Flasker
from Library.ModelModule import UserManager, UserColumnManager
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
from Library.ConstantsModuleF import Constants
from Library.ClubberModule import Clubber
from Library.BeanModule import Cuser
from datetime import datetime, timedelta
from app.email import send_password_reset_email
import random
import jsonpickle


version = '1.7.1'
titles = {'home':'Home Page', 'addMovies':'Add to My Movies', 'displayMovies':'Display My Movies', 'settings':'Settings', 'club':'Movie Clubs Home', 'clubCreate':'Create Movie Club', 'clubManage':'Manage Movie Club', 'contact':'Contact Us'}
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
    flasker = Flasker()
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    if not form.validate_on_submit():
        if 'csrf_token' in request.form:
            # Submit button pressed
            flash('Please enter a login and password')
            
        return render_template('index.html', title='Welcome', sstyle=common, form=form, flasker=flasker, cuser=cuser)
    
    
    user = User.query.filter_by(login=form.login.data).first()
    if user is None or not user.check_password(form.password.data):
        info("Invalid user (" + str(form.login.data) + ") or password")
        flash('Sorry, the login / password combination was not recognized')

        return render_template('index.html', title='Welcome to Goldkeys Movies', sstyle=common, form=form, flasker=flasker, cuser=cuser)
    
  
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
    
    sess = Sessioner(version)
    cuser = sess.get('cuser') 

    latestVersion = getLatestVersion()
    newVersions = getNewVersions()
    
    if len(newVersions) == 0:
        current_user.setLastVisit()

    return render_template('home.html', title='Home Page', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, latestVersion=latestVersion, newVersions=newVersions, cuser=cuser, rand=rand())


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
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    if form.validate_on_submit():
        um = UserManager()
        user = um.addUser(form)
        db.session.commit()
        
        ucm = UserColumnManager()
        ucm.addUserColumns('user', user.id)
        db.session.commit()
        
        info('Registered new user  ' + user.login)
        user.log('register', 'success', '')
        flash('Congratulations, you are now a registered user! Please login.')
        
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', sstyle=common, form=form, cuser=cuser)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    init('reset_password_request')
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('index'))
    return render_template('reset_password_request.html', title='Request Password Reset', sstyle=common, form=form, cuser=cuser)
    
@app.route('/reset_password_change/<token>', methods=['GET', 'POST'])
def reset_password_change(token):   
    init('reset_password_change')
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
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
    
    return render_template('reset_password_change.html', title='Reset Your Password', sstyle=common, form=form, cuser=cuser)

@app.route('/addMovies', methods=['GET', 'POST'])
@login_required
def addMovies():
    info()
    init('addMovies')

    rapid = Rapid()
    
    movies = []
    persons = []
    
    flasker = Flasker()
    
    sess = Sessioner(version)
    searcher = sess.get('searcher')   
    searcher.setArgs(request.args)      
    sess.put('searcher', searcher)
    
    cuser = sess.get('cuser')
    
    action = request.args.get('action', '')
    info('action=' + action)
    
    typeSelect = searcher.addTypeSelect
    addTitleSearch = searcher.addTitle
    addPersonSearch = searcher.addPerson
    addLesserSearch = searcher.addLesser
    
    rankField = request.args.get('rankField', 'rank')
    rankForm = RankListForm()
    rankForm.rankField.default = rankField
    rankForm.process()

    showMine = request.args.get('showMine')
    rankShowMineForm = RankShowMineForm()
    rankShowMineForm.showMineField.data = showMine == 'True'
    
    genreCheckBoxesForm = GenreCheckBoxesForm()
    checkedCodes = request.args.get('checkedCodes', '')
    checkedValues = rapid.getGenreNamesFromCodes(checkedCodes)
    
    
    if action == 'titleSearchRapid':
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
        current_user.log('addMovies', 'popularListGenreRapid', '')
        movies = rapid.listMoviesByGenreRankPopularity(cuser, rankField, showMine, checkedCodes)
            
    return render_template('addMovies.html', title='Add to My Movies', sstyle=Style().getAdderStyle(), user=current_user, flasker=flasker, rankForm=rankForm, rankShowMineForm=rankShowMineForm, addTitleSearch=addTitleSearch, addPersonSearch=addPersonSearch, addLesserSearch=addLesserSearch, typeSelect=typeSelect, persons=persons, genreCheckBoxesForm=genreCheckBoxesForm, rankField=rankField, checkedCodes=checkedCodes, checkedValues=checkedValues, cuser=cuser, movies=movies)


@app.route('/addMoviesOmdb', methods=['GET', 'POST'])
@login_required
def addMoviesOmdb():
    omdb = Omdb()
    addTitleSearch = request.form['addTitleSearch']
    
    sess = Sessioner(version)
    cuser = sess.get('cuser')
        
    current_user.log('addMoviesOmdb', 'addTitleSearch', addTitleSearch)
    movies = omdb.find(cuser, addTitleSearch)
    

    
    response = render_template('addMoviesTable.html', user=current_user, cuser=cuser,  movies=movies)
    return response
    
    
@app.route('/addMoviesOmdbCandidates', methods=['GET', 'POST'])
@login_required
def addMoviesOmdbCandidates():
    omdb = Omdb() 
    addTitleSearch = request.form['addTitleSearch']
    
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    
    omdb.initSpell(addTitleSearch)
    response = render_template('addMoviesCandidates.html', user=current_user, cuser=cuser, omdb=omdb)
    return response

@app.route('/addMovie', methods=['GET', 'POST'])
@login_required
def addMovie():
    displayType = request.form['displayType']
    tt = request.form['tt']

    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    info('addMovie, tt=' + tt + ', displayType=' + displayType)
    init('addMovie')
    
    current_user.log('addMovie', 'tt, displayType', tt + "," + displayType)
    adder = Adder()
    response = adder.addMovie(cuser, displayType, tt )
    
                
    if cuser.user_type == 'club':
        clubber = Clubber()
        clubber.addMovie(cuser, tt)

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
    
    sess = Sessioner(version)
    searcher = sess.get('searcher')
    searcher.setDisplayType(request.args)
    sess.put('searcher', searcher)    
        
    pager = sess.get('pager')   
    cuser = sess.get('cuser') 
    
    bodyHeight = request.args.get('bodHeight', '700')
    
    style = Style()
    sstyle = style.getDisplayStyle(current_user, cuser, searcher.displayType, bodyHeight)
    
    movies = []

    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    

    render = render_template('displayMovies.html', title='Display My Movies', sstyle=sstyle, user=current_user, flasker=flasker, pager=pager, searcher=searcher, cuser=cuser, movies=movies, title_line = 'displayMoviesButtons.html')

    return render

@app.route('/doMovies', methods=['GET', 'POST'])
@login_required
def doMovies():
    info('doMovies')
    current_user.log('doMovies', '', '')
    
    return getMovieResponse(True)

@app.route('/filterMovies', methods=['GET', 'POST'])
@login_required
def filterMovies():
    elementName = request.form['elementName']
    elementValue= request.form['elementValue']

    info('filterMovies, ' + elementName + " = '" + elementValue + "'")
    current_user.log('filterMovies', elementName, elementValue)

    return getMovieResponse(True)

@app.route('/isFiltered', methods=['GET', 'POST'])
@login_required
def isFiltered():
    sess = Sessioner(version)
    searcher = sess.get('searcher')      
    response = str(searcher.hasSearch())

    return response


@app.route('/clearFilters', methods=['GET', 'POST'])
@login_required
def clearFilters():

    info('clearFilters')
    current_user.log('clearFilters', '', '')
    
    return getMovieResponse(True, clearFilters=True)

@app.route('/pageMovies', methods=['GET', 'POST'])
@login_required
def pageMovies():

    info()
    init('pageMovies')
    return getMovieResponse(False)

    
@app.route('/sortMovies', methods=['GET', 'POST'])
@login_required
def sortMovies():
    sortButton = request.form['sortButton']
    info('sortMovies, sortButton=' + sortButton)

    return getMovieResponse(True, sortButton=sortButton)  

@app.route('/changeDisplayType', methods=['GET', 'POST'])
@login_required
def changeDisplayType():

    info()
    init('changeDisplayType')

    return getMovieResponse(True)  

@app.route('/deleteMovie', methods=['GET', 'POST'])
@login_required
def deleteMovie():
    imdb_movie_id = request.form.get('imdb_movie_id')
    
    info('deleteMovie, imdb_movie_id=' + imdb_movie_id) 
    current_user.log('displayMovies', 'delete', imdb_movie_id)
    
    sess = Sessioner(version)
    cuser = sess.get('cuser') 

    display = Display()
    display.deleteMovie(cuser, imdb_movie_id)
    return getMovieResponse(False)  


@app.route('/filterSeries', methods=['GET', 'POST'])
@login_required
def filterSeries():
    
    series = request.form['elementValue']
    
    info('filterSeries, series=' + series) 
    current_user.log('filterSeries', 'series', series)
    

    return getMovieResponse(True) 

def getMovieResponse( resetSearch, clearFilters=False, sortButton=None, bodyHeight=0):
    display = Display()
 
    sess = Sessioner(version)
    searcher = sess.get('searcher')      
    searcher.setArg(request.form)
    
    cuser = sess.get('cuser')

    if clearFilters:
        searcher.clearFilters()
        

    timer = Timer()
    movies = display.displayMovies(current_user, cuser, searcher, sortButton)
    timer.elapse('Found # Movies=' + str(len(movies)))

    numCast = display.getNumCast(cuser, searcher.displayType)

    
    #Saving searcher here because display.displayMovies might have changed it.
    sess.put('searcher', searcher)
    

    pager = sess.get('pager')
    pager.setArg(request.form, resetSearch, searcher, len(movies))    
    sess.put('pager', pager)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    
    moviesFound = flasker.getMoviesFound(len(movies))
    
    clubber = Clubber()
    if cuser.user_type == 'club':
        clubber.setClub(cuser.user_id)
        
    renderBaseTitleLine = render_template('displayMoviesButtons.html', user=current_user, cuser=cuser, flasker=flasker, searcher=searcher)
    renderFoundCell = render_template('displayMoviesFound.html', user=current_user, cuser=cuser, searcher=searcher, moviesFound=moviesFound)
    renderPageCell = render_template('displayMoviesPages.html', user=current_user, cuser=cuser, pager=pager)
    renderSortRow = render_template('displayMoviesSortRow.html', user=current_user, cuser=cuser, flasker=flasker, searcher=searcher)
    renderBody = render_template('displayMoviesBody.html', user=current_user, clubber=clubber, cuser=cuser, flasker=flasker, searcher=searcher, pager=pager, movies=movies, numCast=numCast, personLimit=Constants().personLimit)

    response = {'renderBaseTitleLine': renderBaseTitleLine, 'renderFoundCell': renderFoundCell, 'renderPageCell': renderPageCell,  'renderSortRow' : renderSortRow, 'renderBody' : renderBody}
    return response

@app.route('/movieSeen', methods=['GET', 'POST'])
@login_required
def movieSeen():
    tt = request.args['tt']
    
    info(tt)
    init('movieSeen, tt=' + tt)
    
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    searcher = Searcher()
    searcher.displayType = 'seen'
    
    display = Display()
    movie = display.seen(cuser, tt)
    flasker = Flasker()

    return render_template('movieSeen.html', style=Style().getCommonStyle(), flasker=flasker, user=current_user, searcher=searcher, cuser=cuser, movie=movie )


@app.route('/clubUpdateField', methods=['GET', 'POST'])
@login_required
def clubUpdateField():

    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
    club_id = int(request.form['club_id'])
    user_movie_id = int(request.form['user_movie_id'])
    name = request.form['name']  
    value = request.form['value']  
    dataFormat = request.form['dataFormat']  
    
    clubber = Clubber()
    rtn = clubber.clubUpdateField(cuser, club_id, user_movie_id, name, dataFormat, value)

    return rtn

@app.route('/clubGetCache', methods=['GET', 'POST'])
@login_required
def clubGetCache():
    club_id = int(request.form['club_id'])
    imdb_movie_id = int(request.form['imdb_movie_id'])
    
    clubber = Clubber()
    rtn = clubber.getCache(club_id, imdb_movie_id)

    return jsonify(rtn)


@app.route('/inputField', methods=['GET', 'POST'])
@login_required
def inputField():
    init('inputField')
    
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
    inputter = Inputter()
    
    message = inputter.processInput(cuser,
                        request.form['imdbMovieId'],
                        request.form['name'],
                        request.form['value'],
                        request.form['dataFormat'])
    
    return message

@app.route('/inputSettingsDisplayField', methods=['GET', 'POST'])
@login_required
def inputSettingsDisplayField():
    init('inputSettingsDisplayField') 
    
    sess = Sessioner(version)
    cuser = sess.get('cuser') 

    inputter = Inputter()
    message = inputter.processSettingsDisplayInput(cuser,
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
    
    #if 'user_type' in request.args:
    #   return settings_display() 
   
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    debug('testing setting & settings-expire')
    if not sess.get('settings') or not sess.get('settings-expire'):
        debug('putting setting & settings-expire')
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
        
        return render_template('settings.html', title='Settings', user=current_user, sstyle=common, flasker=flasker, cuser=cuser, settings='none')
       
@app.route('/settings_account', methods=['GET', 'POST'])
@login_required
def settings_account():
    init('settings_account') 
    
    sess = Sessioner(version)
    cuser = sess.get('cuser')
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
        

    return render_template('settings.html', title='Account Settings', sstyle=common, form=form, user=current_user, flasker=flasker, cuser=cuser, settings='account')

@app.route('/settings_display')
@login_required
def settings_display():
    init('settings_display') 
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    sess.put('settings', 'display')
    sess.put('settings-expire', datetime.now() + timedelta(hours=1))

    info('settings, skey=' + sess.get('settings'))
    current_user.log('settings', 'display', '')
    flasker = Flasker()
    
    searcher = sess.get('searcher')
    searcher.setArgs(request.args)  
    sess.put('searcher', searcher)

    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, searcher=searcher, cuser=cuser, settings='display')

@app.route('/settings_display_upCol')
@login_required
def settings_display_upCol():
    info()
    init('settings_display_upCol') 
    selectCol = request.args.get('name')

    sess = Sessioner(version)
    cuser = sess.get('cuser')
    searcher = sess.getWithArgs('searcher', request.args)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.upCol(cuser, selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, settings='display', searcher=searcher, cuser=cuser, selectCol=selectCol)

@app.route('/settings_display_dnCol')
@login_required
def settings_display_dnCol():
    info()
    init('settings_display_dnCol') 
    selectCol = request.args.get('name')

    sess = Sessioner(version)
    cuser = sess.get('cuser')
    searcher = sess.getWithArgs('searcher', request.args)

    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.dnCol(cuser, selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, settings='display', searcher=searcher, cuser=cuser, selectCol=selectCol)


@app.route('/settings_display_resetCol')
@login_required
def settings_display_resetCol():
    info()  
    init('settings_display_resetCol')    
    selectCol = request.args.get('name')

    sess = Sessioner(version)
    cuser = sess.get('cuser')
    searcher = sess.getWithArgs('searcher', request.args)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.resetCol(cuser, selectCol)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common, user=current_user, flasker=flasker, settings='display', searcher=searcher, cuser=cuser, selectCol=selectCol)

@app.route('/settings_display_resetSort')
@login_required
def settings_display_resetSort():
    info()  
    init('settings_display_resetSort')   
    selectCol = ""
    
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    searcher = sess.getWithArgs('searcher', request.args)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.resetSort(cuser)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common,  user=current_user,  flasker=flasker, settings='display', searcher=searcher,  cuser=cuser, selectCol=selectCol)


@app.route('/settings_display_resetAll')
@login_required
def settings_display_resetAll():
    info()    
    init('settings_display_resetAll')    
    selectCol = ""

    sess = Sessioner(version)
    searcher = sess.getWithArgs('searcher', request.args)
    cuser = sess.get('cuser') 
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    flasker.resetAll(cuser)
    
        
    return render_template('settings.html', title='Display Settings', sstyle=common,  user=current_user,  flasker=flasker, settings='display', searcher=searcher, cuser=cuser, selectCol=selectCol)


@app.route('/settings_reset')
@login_required
def settings_reset():
    init('settings_reset') 
    sess = Sessioner(version)
    cuser = sess.get('cuser')
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
        
    return render_template('settings.html', title='Reset Settings', sstyle=common, user=current_user, flasker=flasker, cuser=cuser, settings='reset')



#Movie Club functions xxx
@app.route('/club')
@login_required
def club():
    init('club') 
    info('club')
    
    flasker = Flasker()
    clubber = Clubber()
    clubber.getMyInvites(current_user)
    clubber.getMyMemberships(current_user)
    clubber.getMyOwned(current_user)
    
    cuser = Cuser('club', 0)

    return render_template('club.html', title='Movie Club Home', sstyle=common, user=current_user, flasker=flasker, cuser=cuser, clubber=clubber)

@app.route('/clubCreate', methods=['GET', 'POST'])
@login_required
def clubCreate():
    init('clubCreate') 
    info('clubCreate')
    
    flasker = Flasker()
    clubber = Clubber()
    
    form = ClubCreateForm()

    if form.validate_on_submit():
        club = clubber.create(form, current_user)
        fls = "You successfully created club: '" + club.name + "'."
        flash(fls)
        
        form = ClubManageForm()
        searchForm = ClubSearchForm()
        
        clubber.setClub(club.club_id)
        clubber.getClubInvites()
        clubber.populateClubForm(form)
                
        sess = Sessioner(version)
        cuser = Cuser('club', club.club_id)
        sess.put('cuser', cuser)   
        
        return render_template('clubManage.html', title='Manage Movie Club', sstyle=common, user=current_user, flasker=flasker, form=form, searchForm=searchForm, clubber=clubber, cuser=cuser)
    else:
        cuser = Cuser('club', 0)
        return render_template('clubCreate.html', title='Create Movie Club', sstyle=common, user=current_user, flasker=flasker, form=form, clubber=clubber, cuser=cuser)

    
    
@app.route('/clubManage', methods=['GET', 'POST'])
@login_required
def clubManage():
    init('clubManage') 
    info('clubManage')
    
    club_id = int(request.args.get("club_id"))
    flasker = Flasker()
   
    sess = Sessioner(version)

    
    clubber = Clubber()
    clubber.setClub(request.args.get("club_id"))
    clubber.getClubInvites()
    
    form = ClubManageForm()

    if form.validate_on_submit():
        clubber.updateClub(form)
        flash('Club information updated')
    else:
        clubber.populateClubForm(form)

        
    searchForm = ClubSearchForm()
    if searchForm.validate_on_submit():
        clubber.search(searchForm)

    cuser = Cuser('club', club_id)
    sess.put('cuser', cuser)
    
    return render_template('clubManage.html', title='Manage Movie Club', sstyle=common, user=current_user, flasker=flasker, form=form, searchForm=searchForm, clubber=clubber, cuser=cuser)
     
@app.route('/clubManageSearch', methods=['GET', 'POST'])
@login_required
def clubManageSearch():
    init('clubManageSearch') 
    info('clubManageSearch')
   
    flasker = Flasker()

    clubber = Clubber()
    clubber.setClub(request.args.get("club_id"))
    clubber.getClubInvites()
    
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    form = ClubManageForm()
    form.name.default = clubber.club.name
    form.description.default = clubber.club.description
    form.process() 
        
    searchForm = ClubSearchForm()
    if searchForm.validate_on_submit():
        clubber.search(current_user, searchForm)

    return render_template('clubManage.html', title='Manage Movie Club', sstyle=common, user=current_user, flasker=flasker, form=form, searchForm=searchForm, clubber=clubber, cuser=cuser)
 
 
 
@app.route('/clubInvite', methods=['GET', 'POST'])
@login_required
def clubInvite():
    init('clubInvite') 
    info('clubInvite')
    
    flasker = Flasker()
    sess = Sessioner(version)
    cuser = sess.get('cuser')
    
    clubber = Clubber()
    clubber.invite(current_user, request.args.get("to_user_id"), request.args.get("club_id"))
    
    clubber.setClub(request.args.get("club_id"))
    clubber.getClubInvites()
    
    form = ClubManageForm()
    form.name.default = clubber.club.name
    form.description.default = clubber.club.description
    form.process() 
    
    searchForm = ClubSearchForm()
    return render_template('clubManage.html', title='Manage Movie Club', sstyle=common, user=current_user, flasker=flasker, form=form, searchForm=searchForm, clubber=clubber, cuser=cuser)
   
@app.route('/inviteAnswer', methods=['GET', 'POST'])
@login_required
def inviteAnswer():
    init('inviteAnswer') 
    info('inviteAnswer')

    clubber = Clubber()
    rtn = clubber.inviteAnswer(current_user, request.args.get("invite_id"), request.args.get("answer"))
    flash(rtn)
    return club()
  
@app.route('/displayClub', methods=['GET', 'POST'])
@login_required
def displayClub(): 
    init('displayClub') 
    info('displayClub')
    
    club_id = int(request.args.get("club_id"))
    cuser = Cuser('club', club_id)
    sess = Sessioner(version)
    sess.put('cuser', cuser)
    return displayMovies()

@app.route('/movieReview', methods=['GET', 'POST'])
@login_required
def movieReview():

    club_id =  request.args['club_id']
    imdb_movie_id = request.args['imdb_movie_id']
    
    info('movieSeen')
    init('movieSeen, imdb_movie_id=' + imdb_movie_id)
    
        
    sess = Sessioner(version)
    searcher = sess.get('searcher')
    cuser = Cuser('club', club_id)
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    
    clubber = Clubber()

    clubber.setClubMovie(club_id, imdb_movie_id)
    clubber.makeVerticalDivide(cuser, current_user)
        
    return render_template('movieReview.html', style=Style().getCommonStyle(), flasker=flasker, user=current_user, cuser=cuser, searcher=searcher, clubber=clubber, src='review', rand=rand() )
        



@app.route('/addReviewedMovie', methods=['GET', 'POST'])
@login_required
def addReviewedMovie():
    user_id =  request.args['user_id']
    club_id = request.args['club_id']
    imdb_movie_id = request.args['imdb_movie_id']
     
    info('addReviewedMovie')
    init('addReviewedMovie')
    
    sess = Sessioner(version)
    searcher = sess.get('searcher')
    cuser = sess.get('cuser')
    
    flasker = Flasker()
    flasker.setArgs(current_user, searcher)
    
    clubber = Clubber()
    clubber.addReviewedMovie(user_id, club_id, imdb_movie_id)
    clubber.makeVerticalDivide(cuser, current_user)
        
    return render_template('movieReview.html', style=Style().getCommonStyle(), flasker=flasker, user=current_user, cuser=cuser, searcher=searcher, clubber=clubber, src='review', rand=rand() )
  



@app.route('/clubManageDelete', methods=['GET', 'POST'])
@login_required
def clubManageDelete():
    init('clubManageDelete') 
    info('clubManageDelete')

    club_id = int(request.args['club_id'])
    clubber = Clubber()
    clb = clubber.delete(club_id)
    flash("Club: '" + clb.name + "' has been deleted")
    return club()
    
    
@app.route('/clubExit', methods=['GET', 'POST'])
@login_required
def clubExit():
    init('clubExit') 
    info('clubExit')

    cuser = Cuser('user', current_user.id)
    sess = Sessioner(version)
    cuser = sess.put('cuser', cuser) 

    return redirect(url_for('home'))
    #return home()

@app.route('/allCast', methods=['GET', 'POST'])
@login_required
def allCast():
    tt = request.form['tt']
    info('tt=' + tt)

    display = Display()
    response = display.allCast(tt)
    return response


@app.route('/updateMovies', methods=['GET', 'POST'])
@login_required
def updateMovies():
    info()  
    init('updateMovies')
    
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
    current_user.log('updateMovies', '', '')
    
    adder = Adder()
    oldestForm = UpdateByOldestForm()
    singleForm = UpdateSingleForm()
    rankForm = UpdateRankForm()
    
    oldest_message = ''
    single_message = ''
    rank_message = ''
    
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
        elif request.form.get('submit') == rankForm.submit.label.text:
            #
            # Update Highest Ranked & Most Popular Movies
            #
            rank_message = adder.updateRankandPopularImdbMovies()
        else:
            oldest_message = 'Error: unrecognized submit = ' + str(request.args.get('submit'))
            
    return render_template('updateMovies.html', title='Update Movies', sstyle=common, flasker=Flasker(), oldestForm=oldestForm, singleForm=singleForm, rankForm=rankForm, oldest_message=oldest_message, single_message=single_message, rank_message=rank_message, cuser=cuser, user=current_user)



@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    info()  
    init('contact')
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
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

    return render_template('contact.html', title='Contact Us', user=current_user, flasker=Flasker(), sstyle=common, form=form, sent=sent, cuser=cuser)



@app.route('/asUser', methods=['GET', 'POST'])
@login_required
def asUser():
    info()     
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
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
            
    return render_template('asUser.html', title='Login As User', flasker=Flasker(), sstyle=common, form=form, message=message, cuser=cuser, user=current_user)
 

@app.route('/adminDeleteUser', methods=['GET', 'POST'])
@login_required
def adminDeleteUser():
    info()     
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
    message = []
    form = AdminDeleteUserForm()
    
    if 'csrf_token' in request.form:
        
        adminer = Adminer()
        message = adminer.deleteUser(form.userSelect.data)
            
    return render_template('admin_delete_user.html', title='Delete a User', flasker=Flasker(), sstyle=common, form=form, message=message, cuser=cuser, user=current_user)
 


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
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
    versions = getAllVersions()

    return render_template('versions_all.html', title='Release Notes', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, versions=versions, cuser=cuser)


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

    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
    return render_template('admin.html', title='Administration Functions', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, cuser=cuser)
 
 
@app.route('/updateRelease', methods=['GET', 'POST'])
@login_required
def updateRelease():
    info()
    init('updateRelease')
    sess = Sessioner(version)
    cuser = sess.get('cuser') 
    
    message = ''

    if 'step' in request.args:
        version = request.args['version']
        step = request.args['step']
        us = UpdateRelease()
        message = us.update(version, step)
        info('message = ' + message)
    return render_template('updateRelease.html', title='Update Release', flasker=Flasker(), sstyle=Style().getHomeStyle(), user=current_user, cuser=cuser, message=message)
 
 
 
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


