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

echo 'Generating .nev done !'
echo 'Now, installing nx. Select default choice'

cd src && npm install

echo 'Done'
