from flask import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask.ext.login import LoginManager
from flask.ext.principal import Principal

app = Flask(__name__)
app.config.from_object('config')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy(app)

principals = Principal(app)

lm = LoginManager()
lm.init_app(app)

import MashupMap.views
import MashupMap.models
import Users.views
import Users.models
from Users.admin.views import ModelView, MashupView, MyAdminIndexView
admin = Admin(app,
              name='mashupmap',
              template_mode='bootstrap3',
              base_template='admin/admin_base.html',
              index_view=MyAdminIndexView())
admin.add_view(ModelView(MashupMap.models.Artist, db.session))
admin.add_view(MashupView(MashupMap.models.Mashup, db.session))
