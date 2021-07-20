# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .
RUN python3 -m pip install pipenv
RUN python3 -m pipenv install

COPY web_server web_server
COPY scripts scripts

CMD [ "/bin/bash", "scripts/container_run.sh"]