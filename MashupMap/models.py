from MashupMap import db

artists = db.Table(
    'artists',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('mashup_id', db.Integer, db.ForeignKey('mashup.id'))
)


playlist_songs = db.Table(
    'playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('mashup_id', db.Integer, db.ForeignKey('mashup.id')),
)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    imageURL = db.Column(db.String(2000))

    def __repr__(self):
        return '<Artist %r>' % (self.name)

    def __str__(self):
        return self.name


class Mashup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    author = db.Column(db.String(64), index=True)
    permalink = db.Column(db.String(1000), unique=True)
    date = db.Column(db.DateTime, index=True)
    artists = db.relationship(
        'Artist',
        secondary=artists,
        backref=db.backref('artist_mashups')
        )
    content = db.Column(db.String(1000))
    isBroken = db.Column(db.Boolean, default=False)
    url = db.Column(db.String(1000))
    score = db.Column(db.Integer)
    clean_title = db.Column(db.String(300))

    def __repr__(self):
        return '<Mashup %r>' % (self.title)

    def __str__(self):
        return self.title


class Counters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(10), index=True, unique=True)
    value = db.Column(db.Integer)

    def __repr__(self):
        return self.key + ": " + str(self.value)

    def __init__(self, key, value=0):
        self.key = key
        self.value = value


# Note: Flask-SQLAlchemy converts CamelCase classes to camel_case
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        uselist=False,
        backref=db.backref('profile', uselist=False)
    )
    playlists = db.relationship('Playlist', backref='owner',
                                lazy='dynamic')

    def __repr__(self):
        return '<UserProfile %r>' % (self.id)

    def __str__(self):
        return str(self.id)

    def __init__(self, name=""):
        self.name = name
        favorites = Playlist(name="Favorites")
        db.session.add(favorites)
        self.playlists.append(favorites)
        print(self.playlists)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    songs = db.relationship(
        'Mashup',
        secondary=playlist_songs,
        backref=db.backref('playlists')
    )

    def __repr__(self):
        return '<Playlist %r>' % (self.name)

    def __str__(self):
        return self.name
