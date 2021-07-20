# stdlib
from functools import wraps
import typing
# 3rd party
import flask
import flask_login
from flask_login.config import EXEMPT_METHODS
import werkzeug.exceptions
# local
import web_server.forms as forms
import web_server.model as model
import web_server.views as views


def permission_required(allow: [str]=()) -> typing.Callable:
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if flask.request.method in EXEMPT_METHODS:
                return func(*args, **kwargs)
            elif flask.current_app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)
            elif not flask_login.current_user.is_authenticated:
                return flask.current_app.login_manager.unauthorized()
            elif flask_login.current_user.permission not in allow:
                raise werkzeug.exceptions.Forbidden()
            return func(*args, **kwargs)
        return decorated_view
    return decorator


def login():
    if flask_login.current_user.is_authenticated:
        result = flask.redirect(flask.url_for('home'))
    else:
        login_form = forms.LoginForm()
        if login_form.validate_on_submit():
            candidate_user = flask.request.db_session.query(model.User).filter_by(email=login_form.email.data).one_or_none()
            if candidate_user is None or not candidate_user.check_password(password=login_form.password.data):
                flask.flash('Invalid username or password')
                result = flask.redirect(flask.url_for('login'))
            else:
                flask_login.login_user(user=candidate_user, remember=login_form.remember_me.data)
                flask.flash('Logged in as email {}, remember_me={}'.format(login_form.email.data, login_form.remember_me.data))
                result = flask.redirect(flask.url_for('home'))
        else:
            result = views.login(login_form=login_form)
    return result


def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('home'))


@permission_required(allow=('read', 'write', 'admin',))
def home():
    return views.home()
