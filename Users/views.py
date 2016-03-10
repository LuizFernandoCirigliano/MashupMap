from flask import Blueprint, redirect, url_for, request, abort, render_template
from flask.ext.login import login_user, logout_user
from Users.forms import SignupForm, LoginForm
from Users.models import User
from MashupMap import lm, db

user_api = Blueprint('user_api', __name__)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@user_api.route('/register', methods=['POST', 'GET'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    login=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        form.flash_errors()
        return render_template('signup.html', form=form)


@user_api.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        next_url = request.args.get('next')
        # if not next_is_valid(next_url):
        #     return abort(400)
        return redirect(next_url or url_for('index'))
    else:
        form.flash_errors()
        return render_template('login.html', form=form)


@user_api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
