FROM alpine:3.18

RUN apk update && apk upgrade && \
	apk add python3 py3-pip libpq-dev postgresql-dev gcc python3-dev musl-dev
RUN rm -f /var/cache/apk/*

RUN pip install django django.db psycopg2 django-sslserver pyjwt django-filter \
	tokens websockets

RUN pip install pytz --upgrade
RUN pip install tzdata --upgrade

WORKDIR /backend

CMD ./start_servers.sh

#stock lflandri
#&& python3 manage.py startapp db_test
