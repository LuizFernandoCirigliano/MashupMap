from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from MashupMap.reddit_bot import download_new_submissions
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


download_new_submissions()
