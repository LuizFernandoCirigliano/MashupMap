import flask_admin as admin
import flask_login as login
from flask import redirect, url_for, request
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView as OriginalModelView
from flask_admin.form import SecureForm


class ModelView(OriginalModelView):
    form_base_class = SecureForm
    column_display_all_relations = True

    def is_accessible(self):
        return login.current_user.is_authenticated and \
            login.current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('user_api.login', next=request.url))


class ArtistView(ModelView):
    column_searchable_list = ['name']
    can_view_details = True


class MashupView(ModelView):
    column_exclude_list = ['content', 'permalink']
    column_filters = ['isBroken']
    column_searchable_list = ['title', 'url']
    can_view_details = True


class UserView(ModelView):
    can_create = False
    can_edit = False
    column_exclude_list = ['password']
    column_searchable_list = ['login', 'email']


class RoleView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not (login.current_user.is_authenticated
                and login.current_user.is_admin):
            return redirect(url_for('user_api.login', next=request.url))
        return super(MyAdminIndexView, self).index()
