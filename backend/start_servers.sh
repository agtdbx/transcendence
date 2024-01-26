#!/bin/sh

if [ ! -d /certs ]
then
	mkdir -p /certs
	# openssl genrsa -des3 -out /certs/server.key 1024
	# openssl genrsa -out /certs/server.key 1024
	openssl genrsa -aes256 -passout pass:foobar -out /certs/server.key 2048
	# openssl rsa -in /certs/server.key -out /certs/server.pem
	openssl rsa -in /certs/server.key -passin pass:foobar -out /certs/server.pem
	openssl req -new -nodes -key /certs/server.pem -out /certs/server.csr -subj "/CN=localhost"
	openssl x509 -req -days 365 -in /certs/server.csr -signkey /certs/server.pem -out /certs/server.crt
fi


# # RUN openssl genrsa -des3 -out /certs/server.key 1024
# openssl genrsa -out /certs/server.key 1024
#
# # RUN openssl req -new -nodes -key /certs/server.pem -out /certs/server.csr
# openssl req -new -nodes -key /certs/server.pem -out /certs/server.csr -subj "/CN=localhost"
# openssl x509 -req -days 365 -in /certs/server.csr -signkey /certs/server.pem -out /certs/server.crt

# Config django server
sleep 5
python3 manage.py makemigrations db_test && python3 manage.py migrate


# Start websocket server
python3 manage.py shell < websocket_server/websocket_server.py &

# Start django server
python3 manage.py runsslserver 0.0.0.0:8000
