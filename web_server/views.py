# stdlib
# 3rd party
from flask import render_template
# local


def login(login_form):
    return render_template('login.html', form=login_form)


def home():
    return render_template('home.html')
