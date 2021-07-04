from app import app
from app import db
from datetime import datetime
from flask import render_template
from app.models import Contact
from Library.ConstantsModuleF import Constants
from app.email import send_email
from threading import Thread
from app import mail
from flask_mail import Message

from threading import Thread
from app import app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

    
class Contacter(Constants):
    def __init__(self, user, form):
        self.form = form

        if user.is_authenticated:
            self.login = user.login
        else:
            self.login = ''
            
    def addContact(self):
        contact = Contact(login=self.login, 
                    firstName=self.form.firstName.data, 
                    lastName=self.form.lastName.data, 
                    email=self.form.email.data,
                    subject=self.form.subject.data, 
                    message=self.form.message.data,
                    contact_date=datetime.utcnow())

        db.session.add(contact)
        db.session.commit()
        
        
    def send_contact_email(self):
        subject = 'Goldkeys Movies - Contact Me'
        sender = app.config['MAIL_USERNAME']
        recipients = app.config['ADMINS']
        
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = render_template('contact/contact.txt', contact=self)
        msg.html = render_template('contact/contact.html', contact=self)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        
 