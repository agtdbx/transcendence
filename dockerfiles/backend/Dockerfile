FROM alpine:3.16

RUN apk update && apk upgrade && \
	apk add python3 py3-pip libpq-dev postgresql-dev gcc python3-dev musl-dev\
	openssl
RUN rm -f /var/cache/apk/*

RUN pip install django django.db psycopg2 django-sslserver pyjwt django-filter \
	tokens websockets requests

RUN pip install pytz --upgrade
RUN pip install tzdata --upgrade
RUN pip install Pillow --upgrade

RUN mkdir /certs

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /certs/private.key -out /certs/certificate.crt -subj "/CN=localhost" -sha256

RUN cat /certs/private.key > /certs/cert.pem
RUN cat /certs/certificate.crt >> /certs/cert.pem

WORKDIR /backend

CMD ./start_servers.sh
