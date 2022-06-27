# Pseudo slot spinner game
This is test task.

Hello, in the first, you sould clone rep:
* cloning repository:
```
git clone https://github.com/AktanKasymaliev/gambling-django-project.git
```
* Install and activate virtual enviroment:
```
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```
* Install all requirements: 
```
pip install -r requirements.txt
```

* Create a file settings.ini on self project level, copy under text, and add your value: 
```
[SYSTEM]
DJANGO_KEY=key
DJANGO_DEBUG=True or False
HOST=localhost:8000 or host

[DATABASE]
DATABASE_PASSWORD=password
DATABASE_USER=user
DATABASE_NAME=dbname 
DATABASE_HOST=localhost or host 
DATABASE_PORT=5432 or host-port
```

* This project working on Postgresql, so install it:
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgres postgres-contrib (MacOS) / 
sudo apt-get install postgresql postgresql-contrib (Ubuntu)
sudo -u postgres psql
```
* Enter in your postgresql, and create database:
```
sudo -u postgres psql
CREATE DATABASE <database name>;
CREATE USER <database user> WITH PASSWORD 'your_super_secret_password';
ALTER ROLE <database user> SET client_encoding TO 'utf8';
ALTER ROLE <database user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <database user> SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE <database name> TO '<database user>';
```

* Sync database with Django:
```
- python manage.py makemigrations
- python manage.py migrate
```

* Create superuser
```
- python manage.py createsuperuser
```


* And finally start project: 
```
- python3 manage.py runserver
```