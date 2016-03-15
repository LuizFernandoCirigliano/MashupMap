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

    def __str__(self):
        return self.name


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

    def __init__(self, login, email, password):
        self.login = login
        self.email = email
        self.password = generate_password_hash(password)

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

    def has_permission(self, name):
        """Check out whether a user has a permission or not."""
        permission = Role.query.filter_by(name=name).first()
        # if the permission does not exist or was not given to the user
        if not permission or permission not in self.roles:
            return False
        return True

    @property
    def is_admin(self):
        return self.has_permission('admin')

    # Required for administrative interface
    def __unicode__(self):
        return self.login

    def __str__(self):
        return self.login
