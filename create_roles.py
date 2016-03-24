from MashupMap import db
from Users.models import Role

db.session.add(Role(name='user'))
db.session.add(Role(name='admin'))

db.session.commit()
