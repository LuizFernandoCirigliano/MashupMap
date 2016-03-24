login = input("Type an username:")
email = input("Type an email:")
password = input("Type a password:")

from MashupMap import db
from Users.models import User, Role
adm = Role.query.filter_by(name='admin').first()
u = User(login=login, email=email, password=password)
u.roles.append(adm)
db.session.add(u)
db.session.commit()
