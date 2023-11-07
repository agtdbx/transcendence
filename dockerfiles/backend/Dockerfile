FROM alpine:3.18

RUN apk update && apk upgrade && \
	apk add python3 py3-pip libpq-dev postgresql-dev gcc python3-dev musl-dev
RUN rm -f /var/cache/apk/*

RUN pip install django django.db psycopg2

WORKDIR /backend

CMD sleep 5 && python manage.py makemigrations db_test && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000


#stock lflandri
#&& python3 manage.py startapp db_test
