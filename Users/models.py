from MashupMap import db
from werkzeug.security import generate_password_hash, \
    check_password_hash

roles = db.Table(
    'roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True)


# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), index=True, unique=True)
    email = db.Column(db.String(254), index=True, unique=True)
    password = db.Column(db.String(160))
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users_in_role')
        )

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    # Required for administrative interface
    def __unicode__(self):
        return self.username
