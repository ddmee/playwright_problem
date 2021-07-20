set -a
. ./.env
set +a
docker build --tag webserver .
docker network create server_net
docker run --network server_net --name pg13 -d -p 666:5432 -e POSTGRES_PASSWORD=$SUPER_PASSWORD postgres:13
# This sleep sucks. Wait for postgres to init.
sleep 5
docker run --network server_net --name webserver -d -p 4040:80 --env-file .env webserver
