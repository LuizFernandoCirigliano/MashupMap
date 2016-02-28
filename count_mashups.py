from flask import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy(app)

import MashupMap.views, MashupMap.models

from MashupMap.models import Mashup
print(Mashup.query.count())
