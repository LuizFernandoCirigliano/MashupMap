from flask import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from Users.admin.views import MashupView
from flask.ext.login import LoginManager
from flask.ext.principal import Principal

app = Flask(__name__)
app.config.from_object('config')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy(app)

principals = Principal(app)

lm = LoginManager()
lm.init_app(app)

admin = Admin(app, name='mashupmap', template_mode='bootstrap3')

import MashupMap.views
import MashupMap.models
import Users.views
import Users.models

admin.add_view(ModelView(MashupMap.models.Artist, db.session))
admin.add_view(MashupView(MashupMap.models.Mashup, db.session))
