# stdlib
# 3rd party
from playwright.sync_api import Page
# local
import web_server.commands_lib as commands_lib
import test_lib.common_page as common_page

TITLE = 'Sign In'
URL = common_page.server_url(sub_path='login')
NEXT_URL = common_page.server_url(sub_path='login?next=%2F')

SIGN_IN_BUTTON = "input:has-text(\"Sign In\")"
LOG_OUT_BUTTON = "a:text(\"Logout\")"
LOG_IN_BUTTON =  "a:text(\"Login\")"

# These are only to be used during testing.
READ_USER = dict(email='read@test.com', permission='read', password='read_password')
WRITE_USER = dict(email='write@test.com', permission='write', password='write_password')
ADMIN_USER = dict(email='admin@test.com', permission='admin', password='admin_password')

USERS = (READ_USER, WRITE_USER, ADMIN_USER)


def go_to(page: Page):
    page.goto(URL)
    assert page.title().lower() == TITLE.lower()


def user_exists(email:str):
    for user in commands_lib.list_users():
        if email == user.email:
            return True
    else:
        return False


def user_created(email:str, password:str, permission:str):
    if not user_exists(email=email):
        commands_lib.create_user(email=email, password=password, permission=permission)
        assert user_exists(email=email)


def sign_in(page: Page, email:str='', password:str=''):
    page.fill('#email', email)
    page.fill('#password', password)
    page.click(SIGN_IN_BUTTON)


def sign_in_user(page: Page, user: dict):
    user_created(**user)
    sign_in(page=page, email=user['email'], password=user['password'])


def sign_in_read_user(page: Page):
    sign_in_user(page=page, user=READ_USER)


def sign_in_write_user(page: Page):
    sign_in_user(page=page, user=WRITE_USER)


def sign_in_admin_user(page: Page):
    sign_in_user(page=page, user=ADMIN_USER)


def log_out(page: Page):
    page.click(LOG_OUT_BUTTON)
    assert page.url == NEXT_URL
