#!/bin/sh

# Config django server
sleep 2
python3 manage.py makemigrations db_test && python3 manage.py migrate

# Create defaut user
python3 manage.py shell < db_create_default.py && echo "Karl is back from Hoxes IV." || echo "Karl is dead on Hoxes IV."

# Start websocket server
python3 manage.py shell < websocket_server/websocket_server.py &

# Start django server
python3 manage.py runsslserver 0.0.0.0:8000
