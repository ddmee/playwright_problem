# stdlib
import logging
# 3rd party
import flask
from sqlalchemy import create_engine, MetaData
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
import werkzeug.exceptions
# local
import web_server.settings as settings


default_url = settings.DATABASE_URI.replace('USER', settings.DATABASE_USER).replace('PASSWORD', settings.DATABASE_PASSWORD)
default_engine = create_engine(default_url, convert_unicode=True)
default_metadata = MetaData(bind=default_engine)

read_url = settings.DATABASE_URI.replace('USER', 'read').replace('PASSWORD', settings.DATABASE_READ_PASSWORD)
read_engine = create_engine(read_url, convert_unicode=True)

write_url = settings.DATABASE_URI.replace('USER', 'write').replace('PASSWORD', settings.DATABASE_WRITE_PASSWORD)
write_engine = create_engine(write_url, convert_unicode=True)

admin_url = settings.DATABASE_URI.replace('USER', 'admin').replace('PASSWORD', settings.DATABASE_ADMIN_PASSWORD)
admin_engine = create_engine(admin_url, convert_unicode=True)

# The db sessions to use depending on the permissions of the user
DefaultSession = sessionmaker(bind=default_engine)
AdminSession = sessionmaker(bind=admin_engine)
ReadSession = sessionmaker(bind=read_engine)
WriteSession = sessionmaker(bind=write_engine)
