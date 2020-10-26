from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, State, Country
from flask_login import current_user
from wtforms.widgets import PasswordInput
from wtforms.widgets.core import CheckboxInput
from wtforms.fields.simple import HiddenField
    
def getStateChoices():
    choices = []
    states = State.query.order_by(State.srt).all()
    for state in states:
        choice = (state.state_code, state.state_name)
        choices.append(choice)
    
    return choices        
 
def getCountryChoices():       
    choices = []
    countries = Country.query.order_by(Country.srt).all()
    for country in countries:
        choice = (country.country_code, country.country_name)
        choices.append(choice)
        
    return choices     


class DisplayMoviesForm(FlaskForm):
    titleSearch = StringField('', validators=[DataRequired()])
    genreSearch = StringField('', validators=[DataRequired()])
    actorSearch = StringField('', validators=[DataRequired()])
    plotSearch = StringField('', validators=[DataRequired()])
    
    my_date_seenSearch = StringField('', validators=[DataRequired()])
    my_ratingSearch = StringField('', validators=[DataRequired()])
    my_reviewSearch = StringField('', validators=[DataRequired()])
    
    user01Search = StringField('', validators=[DataRequired()])
    user02Search = StringField('', validators=[DataRequired()])
    user03Search = StringField('', validators=[DataRequired()])
    user04Search = StringField('', validators=[DataRequired()])
    user05Search = StringField('', validators=[DataRequired()])
    user06Search = StringField('', validators=[DataRequired()])
    user07Search = StringField('', validators=[DataRequired()])
    user08Search = StringField('', validators=[DataRequired()])
    user09Search = StringField('', validators=[DataRequired()])
    user10Search = StringField('', validators=[DataRequired()])
 
      
class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    
    city = StringField('City', validators=[])
    stateSelect = SelectField('State', choices=getStateChoices())
    countrySelect = SelectField('Country', choices=getCountryChoices())
    face = FileField('Profile Photo', validators=[])
    
    submit = SubmitField('Register')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Please use a different login, this one is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address used.  Do you already have a login?')
        
        
class SettingsAccountForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    #password = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', widget=PasswordInput(hide_value=False), validators=[DataRequired(), EqualTo('password')])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    
    city = StringField('City', validators=[])
    stateSelect = SelectField('State', choices=getStateChoices())
    countrySelect = SelectField('Country', choices=getCountryChoices())
    face = FileField('Profile Photo', validators=[])

    submit = SubmitField('Update')

    def validate_email(self, email):    
        me = User.query.filter(User.id == current_user.id).first()
        other = User.query.filter(User.email == email.data).first()
        
        if other != None and other.login != me.login:    
            raise ValidationError('Email address used.  Please choose another.')
        
class UpdateByOldestForm(FlaskForm):
    cnt = IntegerField('Count to Update:')
    oldestGenres = BooleanField('Genres:', default=False)
    oldestCast = BooleanField('Cast:', default=False)
    submit = SubmitField('Update Imdb Movies') 
  
class UpdateSingleForm(FlaskForm):
    hidden = HiddenField('hidden')
    tt = StringField('TT:')
    singleGenres = BooleanField('Genres:', default=False)
    singleCast = BooleanField('Cast:', default=False)
    submit = SubmitField('Update Imdb Movie')    
    
class AsUserForm(FlaskForm):
    login = StringField('login:', validators=[DataRequired()])
    submit = SubmitField('Login As User')
 
class AdminDeleteUserForm(FlaskForm):
    choices = []
    
    users = User.query.filter(User.login != 'dflt').order_by(User.lastName).order_by(User.firstName).all()
    for user in users:
        name = user.firstName + ' ' + user.lastName + ' (' + user.login + ")"
        choice = (user.login, name)
        choices.append(choice)
        
    userSelect = SelectField('User: ', choices=choices)
    submit = SubmitField('Delete Selected User')
         
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    

class ResetPasswordChangeForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')  

class ContactForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    firstName = StringField('Name:', validators=[DataRequired()])
    lastName = StringField('', validators=[DataRequired()])
    subject = StringField('Subject:', validators=[DataRequired()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    
    submit = SubmitField('Submit')


  