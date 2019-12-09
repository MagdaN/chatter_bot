Development setup
=================

System prerequisites
--------------------

The application needs Python (`>=3.6`), Git and npm (for development) installed on the machine. The installation depends on your operating system:

### Linux

We recommend to install the prerequisites using the packaging system of your distribution. On Debian/Ubuntu use:

```bash
sudo apt install build-essential python3-dev python3-pip python3-venv
```

### macOS

On macos 10.15 (Catalina) all prerequisites are already installed. On older systems, we recommend to install Python3 and Git using [homebrew](http://brew.sh):

```bash
brew install python3
brew install git
```

### Windows

On Windows, the software prerequisites need to be downloaded and installed from their particular web sites.

For python:
* download from <https://www.python.org/downloads/windows/>
* we recommend a version >= 3.6
* don't forget to check 'Add Python to environment variables' during setup

For git:
* download from <https://git-for-windows.github.io/>

For the Microsoft C++ Build Tools:
* download from <https://wiki.python.org/moin/WindowsCompilers>

All further steps need to be performed using the windows shell `cmd.exe`. You can open it from the Start-Menu.


Application setup
-----------------

Create a virtual environment and install the Python dependencies:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements/dev.txt
```

Create `.env` file with:

```
SECRET_KEY=<key>
DEBUG=True
DATABASE=sqlite:///<database>.sqlite3
```

to use [SQLite](https://www.sqlite.org) as database, or

```
SECRET_KEY=<key>
DEBUG=True
DATABASE=postgresql://<user>:<password>@<host>:<port>/<database>
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
