chatbot
=======

Setup
-----

Create `.env` with:

```
DJANGO_SECRET_KEY=<key>
DJANGO_DEBUG=True
DJANGO_PSQL_DBNAME=<dbname>
DJANGO_PSQL_USER=<user>
DJANGO_PSQL_PASSWORD=<password>
```

Then run:

```
./manage.py sqlcreate        # to obtain the commands to create the database
./manage.py migrate          # to populate the database
./manage.py createsuperuser  # to create an admin user
```

Start the development server using:

```
./manage.py runserver
```
