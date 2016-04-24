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
            print(field)
            if (field == "login_login") | (field == "password_login"):
                for error in errors:
                    flash(u"%s field - %s" % (
                        getattr(form, field).label.text,
                        error
                    ), "login")
            else:
                for error in errors:
                    flash(u"%s field - %s" % (
                        getattr(form, field).label.text,
                        error
                    ), "register")

class LoginForm(FormWithFlash):
    login_login = StringField(
        label="Username",
        validators=[validators.DataRequired(),
                    validators.length(max=254, message="Username too long")],
                    render_kw={"placeholder": "Username"}
    )
    password_login = PasswordField(
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
            self.login_login.errors.append("Invalid User")
            return False
        # Check if password matches
        if not user.check_password(self.password_login.data):
            self.password_login.errors.append('Invalid Login')
            return False
        return True

    def get_user(self):
        logininfo = self.login_login.data
        return User.query.filter(or_(User.login == logininfo,
                                 User.email == logininfo)).first()


class SignupForm(FormWithFlash):
    login_register = StringField(
        label="Username",
        validators=[validators.DataRequired(),
                    validators.length(max=40, message="Username too long")],
                    render_kw={"placeholder": "Username"}
    )
    email_register = EmailField(
        label="Email",
        validators=[validators.DataRequired(),
                    validators.Email(),
                    validators.length(max=254, message="Email too long")],
                    render_kw={"placeholder": "Email"})
    password_register = PasswordField(
        label="Password",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "Password"}
    )
    password_confirmation_register = PasswordField(
        label="Password Confirmation",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "Password Confirmation"}
    )

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.password_confirmation_register.data != self.password_register.data:
            self.password_confirmation_register.errors.append("Passwords don't match")
            return False
        if User.query.filter_by(login=self.login_register.data).count() > 0:
            self.login_register.errors.append('Duplicate username')
            return False
        if User.query.filter_by(email=self.email_register.data).count() > 0:
            self.login_register.errors.append('Duplicate email')
            return False
        return True
