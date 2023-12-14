echo "PGDATA='db_data'" > .env

echo -n "Name for database : "
read dbname
echo "POSTGRES_DB='$dbname'" >> .env

echo -n "User for database : "
read dbuser
echo "POSTGRES_USER='$dbuser'" >> .env

echo -n "Password for database : "
read dbpass
echo "POSTGRES_PASSWORD='$dbpass'" >> .env

echo -n "Django secret key : "
read djangokey
echo "DJANGO_KEY='$djangokey'" >> .env

echo -n "42 api key : "
read apikey
echo "API_KEY='$apikey'" >> .env

echo 'Generating .env done !'
