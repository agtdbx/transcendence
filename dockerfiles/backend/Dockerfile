FROM alpine:3.18

RUN apk update && apk upgrade && \
	apk add python3 py3-pip libpq-dev postgresql-dev gcc python3-dev musl-dev
RUN rm -f /var/cache/apk/*

RUN pip install django psycopg2

WORKDIR /backend

CMD sleep 5 && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
