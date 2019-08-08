Development setup
=================

System prerequisites
--------------------

The application needs Python (`>=3.6`), Git and npm (for development) installed on the machine. The installation depends on your operating system and is covered in [a seperate document](docs/prerequisites).


Development setup
-----------------

Create a virtual environment and install the Python dependencies:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements/dev.txt
```

Create `.env` file with:

```
DJANGO_SECRET_KEY=<key>
DJANGO_DEBUG=True
DJANGO_SQLITE=True
```

to use [SQLite](https://www.sqlite.org) as database, or

```
DJANGO_SECRET_KEY=<key>
DJANGO_DEBUG=True
DJANGO_PSQL_DBNAME=<dbname>
DJANGO_PSQL_USER=<user>
DJANGO_PSQL_PASSWORD=<password>
```

to use [PostgreSQL](https://www.postgresql.org/). See `.env.sample` for all options.

Then run:

```
./manage.py sqlcreate        # to obtain the commands to create the database (postgres only)
./manage.py migrate          # to populate the database
./manage.py createsuperuser  # to create an admin user
```

Start the development server using:

```
./manage.py runserver
```

Install the front-end dependencies and build the static files using:

```
npm install
npm run build
```

Start the webpack watch mode using:

```
npm run watch
```
