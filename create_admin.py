login = input("Type an username:")
email = input("Type an email:")
password = input("Type a password:")

from MashupMap import db
from Users.models import User
u = User(login=login, email=email, password=password)
db.session.add(u)
db.session.commit()
