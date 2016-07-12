from flask import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask.ext.login import LoginManager
from flask_sslify import SSLify
import sys
import logging

app = Flask(__name__, static_url_path='', static_folder='public')
app.config.from_object('config')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

sslifiy = SSLify(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "user_api.login"

import Users.views
import Users.models
import MashupMap.views
import MashupMap.models

from Users.admin.views import MashupView,\
    MyAdminIndexView, UserView, RoleView, ArtistView, ModelView

admin = Admin(app,
              name='mashupmap',
              template_mode='bootstrap3',
              base_template='admin/admin_base.html',
              index_view=MyAdminIndexView())
admin.add_view(ArtistView(MashupMap.models.Artist, db.session))
admin.add_view(MashupView(MashupMap.models.Mashup, db.session))
admin.add_view(ModelView(MashupMap.models.UserProfile, db.session))
admin.add_view(ModelView(MashupMap.models.Playlist, db.session))
admin.add_view(UserView(Users.models.User, db.session))
admin.add_view(RoleView(Users.models.Role, db.session))
admin.add_view(ModelView(MashupMap.models.Counters, db.session))
