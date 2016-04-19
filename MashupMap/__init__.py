from flask import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask.ext.login import LoginManager

app = Flask(__name__, static_url_path='', static_folder='public')
app.config.from_object('config')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

import Users.views
import Users.models
import MashupMap.views
import MashupMap.models

from Users.admin.views import MashupView,\
    MyAdminIndexView, UserView, RoleView, ArtistView
admin = Admin(app,
              name='mashupmap',
              template_mode='bootstrap3',
              base_template='admin/admin_base.html',
              index_view=MyAdminIndexView())
admin.add_view(ArtistView(MashupMap.models.Artist, db.session))
admin.add_view(MashupView(MashupMap.models.Mashup, db.session))
admin.add_view(UserView(Users.models.User, db.session))
admin.add_view(RoleView(Users.models.Role, db.session))
