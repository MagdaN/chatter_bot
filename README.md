chatbot
=======

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

to use [PostgreSQL](https://www.postgresql.org/).

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

Deployment
----------

In production, you should create a dedicated user teh application. All steps for the installation, which do not need root access, should be done using this user. We assume this user is called `django`, it’s home is `/srv/django` and the application is located in `/srv/django/chatter_bot`. The user can be created using:

```bash
# as root
groupadd -g 2000 django
useradd -u 2000 -g 2000 -c 'Django user' -s /bin/bash -d /srv/django -m django
```

Using this user, create a virtual env in the home of this user:

```
# as django
python3 -m venv env

echo "source ~/env/bin/activate" >> ~/.bashrc
. .bashrc
```

Clone the repository and change directory and install the production dependencies:

```
# as django
git clone https://github.com/MagdaN/chatter_bot
cd chatter_bot
```

Install production dependencies:

```
# as django
pip install -r requirements/prod.txt
```

Install the front-end dependencies and build the static files using:

```
npm install
npm run build:prod
```

If `npm` is not available on the server, you can also perform this on a different machine and copy the `/static` directory to the server.

The further deploment with [NGINX](https://www.nginx.com/) and [Gunicorn](https://gunicorn.org/) or [Apache2](https://httpd.apache.org/) is covered in seperate documents:

* [NGINX and Gunicorn](docs/nginx)
* [Apache2](docs/nginx)
