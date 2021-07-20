# local
import web_server.database as database
import web_server.model as model


def create_user(email, password, permission):
    sess = database.AdminSession()
    new_user = model.User(email=email, password_hash='filler', permission=permission)
    new_user.set_password(password=password)
    sess.add(new_user)
    sess.commit()


def remove_user(email):
    sess = database.AdminSession()
    user = sess.query(model.User).filter_by(email=email).one()
    sess.delete(user)
    sess.commit()


def list_users():
    sess = database.AdminSession()
    return sess.query(model.User).all()
