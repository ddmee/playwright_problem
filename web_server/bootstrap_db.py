# stdlib
import argparse
# 3rd party
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
# local
import web_server.settings as settings
import web_server.model as model


def main(super_user: str, super_password: str):

    db_url = settings.DATABASE_URI.replace('USER', super_user).replace('PASSWORD', super_password)
    engine = sqlalchemy.create_engine(db_url, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    engine.execute('CREATE SCHEMA IF NOT EXISTS v1;')

    try:
        engine.execute(f"create user admin with password '{settings.DATABASE_ADMIN_PASSWORD}';")
    except sqlalchemy.exc.ProgrammingError:
        engine.execute(f"alter role admin with password '{settings.DATABASE_ADMIN_PASSWORD}';")
    engine.execute("""grant usage on schema v1 to admin;
    grant create on schema v1 to admin;""")

    model.initialise()

    engine.execute("""grant execute on all functions in schema v1 to admin;
    grant select, insert, update, delete on all tables in schema v1 to admin;
    """)

    try:
        engine.execute("create user {0} with password '{1}';".format(settings.DATABASE_USER, settings.DATABASE_PASSWORD))
    except sqlalchemy.exc.ProgrammingError:
        engine.execute("alter role {0} with password '{1}';".format(settings.DATABASE_USER, settings.DATABASE_PASSWORD))
    engine.execute("""grant usage on schema v1 to {0};
    grant select on all tables in schema v1 to {0};
    grant execute on all functions in schema v1 to {0};
    """.format(settings.DATABASE_USER))

    try:
        engine.execute(f"create user read with password '{settings.DATABASE_READ_PASSWORD}';")
    except sqlalchemy.exc.ProgrammingError:
        engine.execute(f"alter role read with password '{settings.DATABASE_READ_PASSWORD}';")
    engine.execute("""grant usage on schema v1 to read;
    grant select on all tables in schema v1 to read;
    grant execute on all functions in schema v1 to read;
    revoke select on v1.userlist from read;
    """)

    try:
        engine.execute(f"create user write with password '{settings.DATABASE_WRITE_PASSWORD}';")
    except sqlalchemy.exc.ProgrammingError:
        engine.execute(f"alter role write with password '{settings.DATABASE_WRITE_PASSWORD}';")
    engine.execute("""grant usage on schema v1 to write;
    grant select, insert, update, delete on all tables in schema v1 to write;
    grant execute on all functions in schema v1 to write;
    grant usage on all sequences in schema v1 to write;
    revoke select, insert, update, delete on v1.userlist from write;
    """)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup the user roles for the database. Run before running the web server.')
    parser.add_argument('super_password', type=str,
                        help='password for the super user')
    parser.add_argument('--super-user', type=str, default='postgres',
                        help='username for the super user, defaults to postgres')

    args = parser.parse_args()
    main(super_user=args.super_user, super_password=args.super_password)
