# stdlib
# third party
from playwright.sync_api import Page
import pytest
import polling2
import requests
# local
import web_server.commands_lib as commands_lib
from test_lib.common_page import server_url
import test_lib.login_page as login_page


@pytest.fixture(scope='session', autouse=True)
def wait_on_server():
    """Server may not be available at first. Wait on it before running tests"""
    polling2.poll(target=lambda: requests.get(server_url()).status_code == 200,
                  step=1, timeout=30)

@pytest.fixture()
def sign_in_write_user(page: Page):
    user = login_page.WRITE_USER
    login_page.go_to(page=page)
    login_page.sign_in_user(page=page, user=user)
    yield
    login_page.log_out(page=page)
    commands_lib.remove_user(email=user['email'])
