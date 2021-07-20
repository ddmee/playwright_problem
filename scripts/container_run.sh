pipenv run python -m web_server.bootstrap_db $SUPER_PASSWORD --super-user $SUPER_USER
export FLASK_ENV=development
export FLASK_APP=web_server
pipenv run flask run -h 0.0.0.0 -p 80