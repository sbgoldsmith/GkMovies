from app import app
from app import db
from datetime import datetime
from flask import render_template
from app.models import Contact
from Library.ConstantsModuleF import Constants
from app.email import send_email

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
        
        
    def sendEmail(self):
        send_email('Goldkeys Movies - Contact Me',
            sender=app.config['ADMINS'][0],
            recipients=['sgoldsmith@goldkeys.com'],
            text_body=render_template('contact/contact.txt', contact=self),
            html_body=render_template('contact/contact.html', contact=self)
            )
          