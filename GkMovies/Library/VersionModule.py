from flask_login import current_user
from app.models import Version
from Library.LoggerModule import debug

def getLatestVersion():
    lastest = Version.query.order_by(Version.install_date.desc()).first()
    return lastest

def getAllVersions():
    versions = Version.query.order_by(Version.install_date.desc()).all()
    return versions

def getNewVersions():
    new_versions = Version.query.filter(Version.install_date > current_user.last_visit).order_by(Version.install_date.desc()).all()
    debug('Number new versions = ' + str(len(new_versions)))
    return new_versions
