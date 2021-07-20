# stdlib
import contextlib
# 3rd party
from sqlalchemy import Column, BIGINT, Boolean, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from werkzeug.security import generate_password_hash, check_password_hash
# local
import web_server.database as database


Base = declarative_base()


class User(Base):
    __tablename__ = 'userlist'
    __table_args__ = dict(schema='v1')

    id = Column(BIGINT(), primary_key=True, nullable=False)
    email = Column(String(length=120))
    permission = Column(ENUM('read', 'write', 'admin', name='permission_level', schema='v1'))
    password_hash = Column(String(), nullable=True)

    def check_password(self, password):
        return check_password_hash(pwhash=self.password_hash, password=password)

    def set_password(self, password):
        password = password.strip()
        assert len(password) > 8, 'password must be greater than 8 characters'
        self.password_hash = generate_password_hash(password=password)

    # Following are required for flask-login 'is_authenticated', 'is_active', 'is_anonymous', 'get_id'
    @property
    def is_authenticated(self):
        return True

    is_active = Column(Boolean(), default=True, nullable=False)
    is_anonymous = Column(Boolean(), default=False, nullable=False)

    def get_id(self):
        return str(self.id)

    def get_db_session(self):
        if self.permission == 'read':
            sess = database.ReadSession()
        elif self.permission == 'write':
            sess = database.WriteSession()
        elif self.permission == 'admin':
            sess = database.AdminSession()
        else:
            sess = database.DefaultSession()
        return sess

    @contextlib.contextmanager
    def managed_db_session(self):
        sess = self.get_db_session()
        try:
            yield sess
        finally:
            sess.close()


def initialise(engine=database.admin_engine):
    Base.metadata.create_all(engine)
