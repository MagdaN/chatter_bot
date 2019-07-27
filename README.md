chatbot
=======

Setup
-----

Install the front-end dependencies using:

```
npm install
```

Build the static files using:

```
npm run build
```

Create a virtual environment using:

```
python3 -m venv env
source env/bin/activate
```

Install the back-end dependecies using:

```
pip install -r requirements/dev.txt
```

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

Start the webpack watch mode using:

```
npm run watch
```
