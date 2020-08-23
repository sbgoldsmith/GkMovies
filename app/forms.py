from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_login import current_user
from wtforms.widgets import PasswordInput

class AddMoviesForm(FlaskForm):
    titleSearch = StringField('Search By Title:', validators=[DataRequired()])
    
class DisplayMoviesForm(FlaskForm):
    titleSearch = StringField('', validators=[DataRequired()])
    genreSearch = StringField('', validators=[DataRequired()])
    actorSearch = StringField('', validators=[DataRequired()])
    plotSearch = StringField('', validators=[DataRequired()])
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
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
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
    submit = SubmitField('Update')

    def validate_email(self, email):
        print('**** in validate')
        
        me = User.query.filter(User.id == current_user.id).first()
        other = User.query.filter(User.email == email.data).first()
        
        print(me)
        
        if other != None and other.login != me.login:    
            raise ValidationError('Email address used.  Please choose another.')
        
class UpdateForm(FlaskForm):
    fromMovie = IntegerField('From:')
    toMovie = IntegerField('To:')
    submit = SubmitField('Update Imdb Movies')
  
class AsUserForm(FlaskForm):
    login = StringField('login:', validators=[DataRequired()])
    submit = SubmitField('Login As User')
      
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    

class ResetPasswordChangeForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')    