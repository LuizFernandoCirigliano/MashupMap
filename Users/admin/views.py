import flask_admin as admin
import flask_login as login
from flask import redirect, url_for, request
from flask_admin import helpers, expose
from Users.forms import LoginForm
from flask_admin.contrib.sqla import ModelView as OriginalModelView
from flask_admin.form import SecureForm


class ModelView(OriginalModelView):
    form_base_class = SecureForm

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('user_api.login', next=request.url))


class MashupView(ModelView):
    # column_exclude_list = ['content']
    pass


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('user_api.login', next=request.url))
        return super(MyAdminIndexView, self).index()
