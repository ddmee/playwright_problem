# stdlib
# third party
from playwright.sync_api import Page
import pytest
# local
import web_server.commands_lib as commands_lib
import test_lib.login_page as login_page


@pytest.fixture()
def sign_in_write_user(page: Page):
    user = login_page.WRITE_USER
    login_page.go_to(page=page)
    login_page.sign_in_user(page=page, user=user)
    yield
    login_page.log_out(page=page)
    commands_lib.remove_user(email=user['email'])
