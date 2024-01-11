#!/bin/sh

# Start websocket server
python3 websocket_server/websocket.py &

# Start django server
sleep 5
python3 manage.py makemigrations db_test
python3 manage.py migrate
python3 manage.py runsslserver 0.0.0.0:8000
