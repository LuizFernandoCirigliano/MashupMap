import sys

if len(sys.argv) != 4:
    print("Formato: python create_admin.py login email senha")
else:
    from flask import Flask
    from flask.ext.cache import Cache
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config.from_object('config')

    db = SQLAlchemy(app)
    from Users.models import User
    args = str(sys.argv)
    u = User(login=args[1], email=args[2], password=args[3])
    db.session.add(u)
    db.session.commit()
