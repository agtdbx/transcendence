#!/bin/sh

# Config django server
sleep 2
python3 manage.py makemigrations db_test && python3 manage.py migrate

# Start websocket server
python3 manage.py shell < websocket_server/websocket_server.py &

python3 manage.py shell < karl_creator.py && echo "Karl is back from Hoxes IV." || echo "Karl is dead on Hoxes IV."

# Start django server
python3 manage.py runsslserver 0.0.0.0:8000
