# 3rd party
from environs import Env

env = Env(expand_vars=True)
env.read_env()

ENV = env.str("ENV")
DEBUG = env.str("DEBUG")
DATABASE_USER = env.str("DATABASE_USER")
DATABASE_PASSWORD = env.str("DATABASE_PASSWORD")
DATABASE_URI = env.str("DATABASE_URI")

# database user passwords
DATABASE_READ_PASSWORD = env.str("DATABASE_READ_PASSWORD")
DATABASE_WRITE_PASSWORD = env.str("DATABASE_WRITE_PASSWORD")
DATABASE_ADMIN_PASSWORD = env.str("DATABASE_ADMIN_PASSWORD")

# For flask to sign cookies with, so user cannot modify them
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
SESSION_SECRET_KEY = env.str("SESSION_SECRET_KEY")
# Used during generate_crsf() in flask-wtf library.
WTF_CSRF_SECRET_KEY = env.str("WTF_CSRF_SECRET_KEY")
WTF_CSRF_FIELD_NAME = env.str("WTF_CSRF_FIELD_NAME")
# Used validate_csrf(), number of seconds token is valid for
WTF_CSRF_TIME_LIMIT = env.int("WTF_CSRF_TIME_LIMIT", default=3600*24)
