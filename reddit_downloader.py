from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from MashupMap.reddit_bot import download_top_submissions, artist_list_from_title, download_new_submissions
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


download_new_submissions()
# print(artist_list_from_title('Coming Undone (Korn, Taylor Swift) - [3:58]'))
