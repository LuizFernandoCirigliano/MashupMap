from models import Role
from MashupMap import db

db.session.add(Role('user'))
db.session.add(Role('admin'))

db.session.commit()
