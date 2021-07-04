from app import app
from app import db
from datetime import datetime, timedelta
from Library.ConstantsModuleF import Constants
from Library.ModelModule import UserColumnManager
from Library.HelperModuleF import Process, formatDate, formatFloat, tf, isTf
from Library.BeanModule import Cuser
from Library.AdderModuleF import Adder
from Library.FlaskModule import Flasker
from app.models import User, Club, Invite, ClubUser, ClubUserMovie, ImdbMovie, load_club, load_user, load_user_movie, load_imdb_movie, UserMovie, PersonMovie, ClubCache
from sqlalchemy import and_, or_
from flask import Markup
from werkzeug.utils import secure_filename
from flask_login import current_user
import os 
        
def getHeight(rows):
    if rows == 1:
        return 27
    else:
        return 27 + (rows-1) * 13
        
class Clubber(Constants):
    def __init__(self):
        self.club = None
        
    def create(self, form, user):
        club = Club(name = form.name.data, 
                    description = form.description.data, 
                    owner_id = user.id,
                    status = 'active',
                    header = '',
                    allow_add_seen = 'F',
                    allow_add_want = 'T',
                    allow_update = 'T',
                    date_created = datetime.utcnow())
    
        db.session.add(club)
        db.session.commit()
        
        ucm = UserColumnManager()
        ucm.addUserColumns('club', club.club_id)
        db.session.commit()
        
        clubUser = ClubUser(
                    club_id = club.club_id, 
                    user_id = user.id, 
                    status = "active",
                    date_accepted = datetime.utcnow(),
                    date_deleted = None
                    )
        db.session.add(clubUser)
        db.session.commit()
        self.setClub(club.club_id)
        

        return club
        
    #.filter(or_(User.lastName.like("%" + searchForm.searchText.data + "%"), User.firstName.like("%" + searchForm.searchText.data + "%"))\   
    def search(self, current_user, searchForm):
        srch = '%' + searchForm.searchText.data + '%'
        self.matched = User.query\
            .filter(or_(User.lastName.like(srch), User.firstName.like(srch)))\
            .order_by(User.lastName)\
            .order_by(User.firstName)\
            .all()
        
        self.getMyInvites(current_user);
       
        for user in self.matched:
            if self.isMember(user):
                user.clubInviteStatus = 'Current Member'
            elif self.isInvited(user):
                user.clubInviteStatus = 'Invitation Pending'
         
            
    def isMember(self, user):
        for clubUser in self.club.clubUsers:
            if clubUser.user_id == user.id:
                return True
        return False
    
    def isInvited(self, user):
        for invite in self.clubInvites:
            if user.id == invite.to_user_id:
                return True
        return False

    
    def getMyOwned(self, user):
        self.myOwned = Club.query.filter(Club.owner_id == user.id, Club.status == 'active').order_by(Club.date_created).all()
    
    def getMyMemberships(self, user):
        clubUsers = ClubUser.query.filter(ClubUser.user_id == user.id).order_by(ClubUser.date_accepted).all()
        self.myMemberships = []
        for clubUser in clubUsers:
            if clubUser.club.status == 'active':
                self.myMemberships.append(clubUser)
                   
    def getMyInvites(self, user):
        # and_ pending
        invites = Invite.query.filter(Invite.to_user_id == user.id, Invite.status == 'pending').order_by(Invite.date_sent).all()

        self.myInvites = []
        for invite in invites:
            myInvite = InviteDetails()
            myInvite.invite = invite
            myInvite.fromUser = User.query.filter(User.id == invite.from_user_id).first()
            myInvite.club = Club.query.filter(Club.club_id == invite.type_id).first()
            myInvite.sdate = '{d.month}/{d.day}/{d.year}'.format(d=invite.date_sent) 
            self.myInvites.append(myInvite)
            
        return self.myInvites
    
    def getClubInvites(self):
        self.clubInvites = Invite.query.filter(Invite.type == 'club', Invite.type_id == self.club.club_id, Invite.status == 'pending').order_by(Invite.date_sent).all()
        for clubInvite in self.clubInvites:
            clubInvite.user = User.query.filter(User.id == clubInvite.to_user_id).first()
            
    def invite(self, user, to_user_id, type_id):
        invite = Invite(
                    from_user_id = user.id, 
                    to_user_id = to_user_id, 
                    type ="club",
                    type_id = type_id,
                    status = "pending",
                    date_sent = datetime.utcnow(),
                    date_first_read = None,
                    date_changed = None)
        db.session.add(invite)
        db.session.commit()   
        
    def inviteAnswer(self, user, invite_id, answer):
        invite = Invite.query.filter(Invite.invite_id == invite_id).first()
        invite.status = answer
        invite.date_changed = datetime.utcnow()
        db.session.commit()
        
        club =  load_club(invite.type_id)
        
        if answer == 'accept':
            clubUser = ClubUser(club_id = invite.type_id, 
                                user_id = user.id,
                                status = "active",
                                date_accepted = datetime.utcnow(),
                                date_deleted = None)
            db.session.add(clubUser)
            db.session.commit()
            
            
        if answer == 'accept':
            rtn = 'accepted'
        elif answer == 'decline':
            rtn = 'declined'
        else:
            rtn = ''
        
        rtn = "You have " + rtn + " an invitation to join club: '" + club.name + "'."
        return rtn;
    
    
    def setClub(self, club_id):
        self.club =  Club.query.filter(Club.club_id == club_id).first()

    def setClubMovie(self, club_id, imdb_movie_id):
        self.userMovie = UserMovie.query.filter(UserMovie.user_type == 'club', UserMovie.user_id == club_id, UserMovie.imdb_movie_id == imdb_movie_id).first()        
        self.imdbMovie = load_imdb_movie(imdb_movie_id)
        self.club = load_club(club_id)
        self.clubUsers = ClubUser.query.filter(ClubUser.club_id == club_id, ClubUser.status == 'active').all()
        self.setClubUserMovies(club_id, imdb_movie_id)


    def setClubUserMovies(self, club_id, imdb_movie_id):
                
        self.clubUserMovies = ClubUserMovie.query.filter(ClubUserMovie.club_id == club_id, UserMovie.imdb_movie_id == imdb_movie_id, UserMovie.user_type == 'user')\
            .join(UserMovie)\
            .join(User)\
            .order_by(User.lastName)\
            .order_by(User.firstName)\
            .all()
    
    
    def clubUpdateField(self, cuser, club_id, user_movie_id, name, dataFormat, value):

        srtn = ''
      
        userMovie = UserMovie.query.filter(UserMovie.id == user_movie_id)
        column = getattr(UserMovie, name)
        process = Process()
        rtn = process.value(value, dataFormat)
        

        if rtn.message == '':
            userMovie.update({column: rtn.value})  
        elif rtn.message != 'silent':
            srtn = rtn.message
            
        
        db.session.commit()
            
        userMovie = userMovie.first()
        if name == 'my_rating' and userMovie.user_type == 'user':
            self.setGroupRating(club_id, userMovie)
            srtn = self.getGroupRating()
         
            
        self.cacheUpdate(club_id, userMovie, name, dataFormat, value)
          
        return srtn
    
    
    
    def cacheUpdate(self, club_id, userMovie, name, dataFormat, value):
        process = Process()
        rtn = process.value(value, dataFormat)
        if rtn.message != '':
             # Don't update on error.
             return
        
        cache = ClubCache.query.filter(ClubCache.user_movie_id == userMovie.id, ClubCache.name == name).first()
        if not cache:
            cache = ClubCache(
                            club_id = club_id,
                            user_type = userMovie.user_type, 
                            user_id = userMovie.user_id,
                            user_movie_id = userMovie.id,
                            imdb_movie_id = userMovie.imdb_movie_id,
                            name = name,
                            dataFormat = dataFormat)
            db.session.add(cache)

        cache.current_user_id = current_user.id
        cache.value = rtn.value
        cache.cache_time = datetime.utcnow()
        db.session.commit()
        
        older = datetime.utcnow() + timedelta(minutes = -1)
        stmt = ClubCache.__table__.delete().where(and_(ClubCache.current_user_id == current_user.id, ClubCache.cache_time < older))
        db.session.execute(stmt)
        db.session.commit()       
             
    def makeVerticalDivide(self, cuser, user):
        editCols = []
        self.section1 = []
        self.section2 = []
        
        cols = user.getColumns(cuser, 'seen')
        height = 2
        for col in cols:
            if col.vis == 'T' and col.attribute.editable == 'T':
                editCols.append(col)
                height += getHeight(col.rows)
            
        half = height / 2
        heightSoFar = 2

        for col in editCols:
            
            if heightSoFar < half:
                self.section1.append(col)
            else:
                self.section2.append(col)
            heightSoFar += getHeight(col.rows)
            

    def getDisabled(self, user_id):
        if current_user.id == self.club.owner_id or user_id == current_user.id:
            rtn = ''
        else:
            rtn = ' disabled '
        return rtn
    
    def isAllowedUpdate(self, user_id):
        if self.club == None or user_id == self.club.owner_id or self.club.allow_update == 'T':
            return ''
        else:
            rtn = ' disabled '
        return rtn  

    def updateClub(self, form):
        self.club.name = form.name.data
        self.club.description = form.description.data
        self.club.allow_add_seen = tf(form.allow_add_seen.data)
        self.club.allow_add_want = tf(form.allow_add_want.data)
        self.club.allow_update = tf(form.allow_update.data)
                                        
        f = form.header.data
        filename = secure_filename(f.filename)

        if filename != '':
            f.save(os.path.join(self.clubPath, filename))
            self.club.header = filename
            
        db.session.commit()
        

    def canChangeToSeen(self, user, cuser, displayType, club):
        if displayType == 'seen':
            return False
        elif cuser.user_type == 'user':
            return True
        else:
            return user.id == club.owner_id

    def addMovie(self, cuser, tt):
        club = load_club(cuser.user_id)
        adder = Adder()
        # At this point, movie was already added to user_movie, with user_type = club
        # First, get the relevant objects
        imovie = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
        cumovie = UserMovie.query.filter(UserMovie.user_type == 'club',
                                        UserMovie.user_id == cuser.user_id, 
                                        UserMovie.imdb_movie_id == imovie.id).first()


        
        # Add self referential ClubUserMovie so that when in club mode, we can see the review label
        clubUserMovie = ClubUserMovie(
                                club_id = cuser.user_id, 
                                user_movie_id = cumovie.id
                                )
        db.session.add(clubUserMovie)
        db.session.commit()
        cumovie.club_user_movie_id = clubUserMovie.club_user_movie_id
            

                
    def addReviewedMovie(self, user_id, club_id, imdb_movie_id):
        self.setClubMovie(club_id, imdb_movie_id)
        cuser = Cuser('user', user_id)
        
        adder = Adder()
        userMovie = adder.addMovieToUser(cuser, self.imdbMovie, 'seen')

        clubUserMovie = ClubUserMovie(
                                club_id = self.club.club_id, 
                                user_movie_id = userMovie.id
                                )
        db.session.add(clubUserMovie)
        db.session.commit()
        
        self.setClubUserMovies(club_id, imdb_movie_id) 
       
    def populateReviewForm(self, form):
        i=1
        
    def populateClubForm(self, form):
        form.name.default = self.club.name
        form.description.default = self.club.description  
        form.allow_add_seen.default = isTf(self.club.allow_add_seen)
        form.allow_add_want.default = isTf(self.club.allow_add_want)
        form.allow_update.default = isTf(self.club.allow_update)
        form.process()
        
        
    def setGroupRating(self, club_id, userMovie):
        #userMovie is the user's movie record and self.userMovie is for the club
        self.userMovie = UserMovie.query.filter(UserMovie.user_type == 'club', UserMovie.user_id == club_id, UserMovie.imdb_movie_id == userMovie.imdb_movie_id).first()        
        
        total = 0
        cnt = 0
        self.setClubUserMovies(club_id, userMovie.imdb_movie_id)
        for clubUserMovie in self.clubUserMovies:
            if clubUserMovie.userMovie and clubUserMovie.userMovie.my_rating > 0:
                total += clubUserMovie.userMovie.my_rating
                cnt += 1

        if cnt > 0:
            avg = format(float(total) / float(cnt))
        else:
            avg = 0
        
        self.userMovie.my_rating = avg        
        db.session.commit()
        
        flasker = Flasker()
        svalue = flasker.formatValue('number', avg)
        
        self.cacheUpdate(club_id, self.userMovie, 'my_rating', 'number', svalue)
 
    def getGroupRating(self):
        
        if self.userMovie.my_rating == 0:
            avg = '-'
        else:
            avg ="{:.2f}".format(self.userMovie.my_rating)

        return '==' + str(self.userMovie.id) + '_' + str(avg)
    

    def getCache(self, club_id, imdb_movie_id):
       
        flasker = Flasker()
        rtn = []
        caches = ClubCache.query.filter(ClubCache.club_id == club_id, ClubCache.imdb_movie_id == imdb_movie_id, ClubCache.current_user_id != current_user.id).all()

        for cache in caches:
            key = cache.name + '_' + str(cache.user_movie_id)
            value = flasker.formatValue(cache.dataFormat, cache.value)
            tup = (key, value)
            rtn.append(tup)
        
        return rtn
    
    
    def allCast(self, tt):
        #rtn = "<div class='scrollable' style='height:100%'>\n"
        rtn = "<table cellspacing='0' cellpadding='0' style='border:0;'>\n"
        personMovies = PersonMovie.query.filter(PersonMovie.tt == tt, PersonMovie.role == 'actor').order_by(PersonMovie.srt).all()
        for personMovie in personMovies:
            rtn += "<tr style='background-color:transparent;'>\n"
            rtn += "<td style='border:0;text-align:left;width:30px;'>\n"
            rtn += "<a href='https://www.imdb.com/name/" + personMovie.nm + "'  target='_blank'><img src='/static/images/imdb.jpg' style='width:25px'></a>\n"
            rtn += "</td>\n"
            rtn += "<td style='border:0;text-align:left;'>\n"
            rtn += "<a href='https://www.imdb.com/name/" + personMovie.nm + "' class='imdb' target='_blank'>" + personMovie.person.name + "</a>\n"
            rtn += "</td>\n"
            rtn += "</tr>\n"
        rtn += "</table>\n"
        #rtn += "</div>"
        return Markup(rtn)
    
    def delete(self, club_id):
        club = load_club(club_id)
        club.status = 'deleted'
        db.session.commit()
        return club
    
    def getMovieClubs(self, cuser, movie):
        clubs = []
        
        if cuser.user_type == 'user':
            for clubUserMovie in movie.clubUserMovies:
                clubs.append(clubUserMovie.club)
        else:
            clubs.append(load_club(cuser.user_id))
            
        return clubs

            
    def formatDate(self, value):
        return formatDate(value)
    
    def formatFloat(self, value):
        return formatFloat(value)
    
class InviteDetails(Constants): 
    def __init__(self):    
        self.invite = None  
        self.fromUser = None
        self.club = None
        self.sdate = ''