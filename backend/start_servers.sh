#!/bin/sh

# Config django server
sleep 5
python3 manage.py makemigrations db_test && python3 manage.py migrate


# Start websocket server
python3 manage.py shell < chat_server/chat_server.py &

python3 manage.py shell < karl_creator.py && echo "Karl is back from Hoxes IV." || echo "Karl is dead on Hoxes IV."

# Start django server
python3 manage.py runsslserver 0.0.0.0:8000
