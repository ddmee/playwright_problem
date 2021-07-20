# stdlib
# 3rd party
import pytest
# local
import web_server.commands_lib as commands_lib
import test_lib.common_page as common_page
import test_lib.login_page as login_page


def test_index_redirect(page):
    # Should sent to the sign in page, when not logged in
    # rather than the index.
    page.goto(common_page.server_url())
    assert page.title() == login_page.TITLE


def test_no_creds(page):
    login_page.go_to(page=page)
    # Should be rejected when try to sign in without username/password
    login_page.sign_in(page=page)
    # Page purl should not have changed.
    assert page.url == login_page.URL
    # There should be two fields, for email and password boxes, saying these
    # fields are required
    element_list = page.query_selector_all(common_page.FIELD_REQUIRED)
    assert len(element_list) == 2


def test_email_only(page):
    login_page.go_to(page=page)
    login_page.sign_in(page=page, email='bogus@gmail.com')
    # Page url should not have changed.
    assert page.url == login_page.URL
    # Only the password is missing, so should only show one field required
    element_list = page.query_selector_all(common_page.FIELD_REQUIRED)
    assert len(element_list) == 1


def test_bad_email_and_password(page):
    login_page.go_to(page=page)
    login_page.sign_in(page=page, email='bogus@gmail.com', password='thisisbad')
    # Page url should not have changed.
    assert page.url == login_page.URL


@pytest.mark.parametrize('user', login_page.USERS)
def test_login_as_user(page, user):
    login_page.go_to(page=page)
    login_page.sign_in_user(page=page, user=user)
    # should be redirected to the index
    assert page.url == common_page.server_url()
    # top right should state user is logged in
    element_list = page.query_selector_all(f"text='User: {user['email']}'")
    assert len(element_list) == 1
    # assert there is a logout button, by logging out
    login_page.log_out(page=page)
    # and remove the user
    commands_lib.remove_user(email=user['email'])
    assert login_page.user_exists(email=user['email']) is False
