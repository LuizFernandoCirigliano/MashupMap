from MashupMap import db
from flask.ext.wtf import Form
from flask import flash
from wtforms import StringField, PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField
from Users.models import User
from sqlalchemy import or_


class FormWithFlash(Form):
    def flash_errors(form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))


class LoginForm(FormWithFlash):
    login = StringField(
        label="Username",
        validators=[validators.DataRequired(),
                    validators.length(max=254, message="Username too long")],
                    render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        label="Password",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "Password"}
    )

    def validate(self):
        rv = Form.validate(self)
        # Check if fields are complete
        if not rv:
            return False
        user = self.get_user()
        # Check if user exists
        if user is None:
            self.login.errors.append("Invalid User")
            return False
        # Check if password matches
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid Login')
            return False
        return True

    def get_user(self):
        logininfo = self.login.data
        return User.query.filter(or_(User.login == logininfo,
                                 User.email == logininfo)).first()


class SignupForm(FormWithFlash):
    login = StringField(
        label="Username",
        validators=[validators.DataRequired(),
                    validators.length(max=40, message="Username too long")],
                    render_kw={"placeholder": "Username"}
    )
    email = EmailField(
        label="Email",
        validators=[validators.DataRequired(),
                    validators.Email(),
                    validators.length(max=254, message="Email too long")],
                    render_kw={"placeholder": "Email"})
    password = PasswordField(
        label="Password",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "Password"}
    )
    password_confirmation = PasswordField(
        label="Password Confirmation",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "Password Confirmation"}
    )

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.password_confirmation.data != self.password.data:
            self.password_confirmation.errors.append("Passwords don't match")
            return False
        if db.User.filter_by(login=self.login.data).count() > 0:
            self.login.errors.append('Duplicate username')
            return False
        if db.User.filter_by(email=self.email.data).count() > 0:
            self.login.errors.append('Duplicate email')
            return False
        return True
