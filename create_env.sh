echo -n "Name for database : "
read dbname
echo -n "User for database : "
read dbuser
echo -n "Password for database : "
read dbpass

echo "PGDATA=db_data" > .env
echo "POSTGRES_DB=$dbname" >> .env
echo "POSTGRES_USER=$dbuser" >> .env
echo "POSTGRES_PASSWORD=$dbpass" >> .env

npm install --global nx@latest

echo 'Generating done !'
