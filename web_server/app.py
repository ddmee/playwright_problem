# stdlib
# 3rd party
import flask
import flask_login
from flask_wtf.csrf import CSRFProtect
# local
import web_server.database as database
import web_server.forms as forms
import web_server.model as model
import web_server.routes as routes


csrf = CSRFProtect()
login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'


def open_db():
    if flask_login.current_user.is_authenticated:
        sess = flask_login.current_user.get_db_session()
    else:
        sess = database.DefaultSession()
    flask.request.db_session = sess


def close_db(response):
    flask.request.db_session.close()


@login_manager.user_loader
def load_user(user_id: str):
    try:
        sess = database.DefaultSession()
        return sess.query(model.User).filter_by(id=user_id).one_or_none()
    finally:
        sess.close()


def create_app():
    """Application factory for the app"""
    app = flask.Flask(__name__)
    app.config.from_object("web_server.settings")
    app.secret_key = app.config['SESSION_SECRET_KEY']

    model.initialise()

    app.before_request(open_db)
    app.teardown_request(close_db)

    # Initialising sea surf protection. Basically provides jinja with crsf_token() method.
    csrf.init_app(app)
    app.jinja_env.globals['csrf_fieldname'] = app.config['WTF_CSRF_FIELD_NAME']

    # init the login manager
    login_manager.init_app(app)

    app.route('/')(routes.home)
    app.route('/login', methods=['GET', 'POST'])(routes.login)
    app.route('/logout')(routes.logout)

    return app