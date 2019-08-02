Apache and mod_wsgi
-------------------

Install the Apache server and mod_wsgi on Debian or Ubuntu using:

```
sudo apt install apache2 libapache2-mod-wsgi-py3
```

Next, create a virtual host configuration in `/etc/apache2/sites-available/000-default.conf`:

```
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    Alias /static /srv/django/chatter_bot/static_root/
    <Directory /srv/django/chatter_bot/static_root/>
        Require all granted
    </Directory>

    WSGIDaemonProcess django user=django group=django \
        home=/srv/django/chatter_bot python-home=/srv/django/env
    WSGIProcessGroup django
    WSGIScriptAlias / /srv/django/chatter_bot/config/wsgi.py process-group=django
    WSGIPassAuthorization On

    <Directory /srv/django/chatter_bot/config/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

Restart the Apache server: `sudo service apache2 restart`. The application should now be available on `YOURDOMAIN`. Note that the Apache user needs to have access to `/srv/django/chatter_bot/static_root/`.

As you can see from the virtual host configurations, the static assets such as CSS and JavaScript files are served independently from the WSGI-python script. In order to do so, they need to be gathered in the `static_root` directory. This can be achieved by running:

```bash
python manage.py collectstatic
```

in your virtual environment.

In order to apply changes to the code, the webserver needs to be reloaded or the `config/wsgi.py` file needs to appear modified. This can be done using the `touch` command:

```bash
touch config/wsgi.py
```

Also, the `collectstatic` command has to be executed again.
