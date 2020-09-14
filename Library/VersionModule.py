from flask_login import current_user
from app.models import Version


def getLatestVersion():
    lastest = Version.query.order_by(Version.install_date.desc()).first()
    return lastest

def getAllVersions():
    versions = Version.query.order_by(Version.install_date.desc()).all()
    return versions

def getNewVersions():
    new_versions = Version.query.filter(Version.install_date > current_user.last_visit).order_by(Version.install_date.desc()).all()
    return new_versions
