from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from MashupMap.models import Mashup
from urllib import parse


def get_url_from_embed(embed_code):
    try:
        url_start = embed_code.index("url=") + 4
        url_end = embed_code.index("&", url_start)
        url = embed_code[url_start:url_end]
        url = parse.unquote(url)
        print("url found")
        print(url)
        return url
    except ValueError:
        try:
            url_start = embed_code.index("src=\"") + 5
            url_end = embed_code.index("\"", url_start)
            url = embed_code[url_start:url_end]
            url = parse.unquote(url)
            print("url found")
            print(url)
            return url
        except:
            print("url not found")
            print(embed_code)
            return None

mashups = Mashup.query.all()
for m in mashups:
    m.url = get_url_from_embed(m.content)
db.session.commit()
