from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Mail, Message

import logging
from logging.handlers import SMTPHandler
from multiprocessing.pool import job_counter

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'index'
mail = Mail(app)

#
# Initialize logging 
#
from werkzeug._internal import _logger
if _logger:
    _logger.setLevel(50) 
logging.addLevelName(25, 'TIMER')
logging.basicConfig(level=logging.INFO, format='*** GKM %(asctime)s %(levelname)s %(message)s')


#
# Initialize Error Mail Handler
#
class MySMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
 
        Format the record and send it to the specified addressees.
        """
        try:
            print("Starting MySMTPHandler")
            import smtplib
            import string # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
                

            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            print("Starting smtplib.SMTP_SSL")
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            #string.join(self.toaddrs, ","),
                            self.toaddrs[0],
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.login(self.username, self.password)
            print("Starting smtp.sendmail")
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
            
logger = logging.getLogger()

mail_handler = MySMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']), 
                             app.config['MAIL_USERNAME'], 
                             app.config['ADMINS'],
                             'Goldkeys Movies Error', 
                             (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))


mail_handler.setLevel(logging.ERROR)
logger.addHandler(mail_handler)


from app import routes, models, errors
from Library._TestModule import test


with app.app_context():
    test()


