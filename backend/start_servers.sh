#!/bin/sh

# Config django server
sleep 5
python3 manage.py makemigrations db_test
python3 manage.py migrate

# Start websocket server
python3 manage.py shell < websocket_server.py &

# Start django server
python3 manage.py runsslserver 0.0.0.0:8000
