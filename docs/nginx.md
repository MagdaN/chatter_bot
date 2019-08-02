Nginx and Gunicorn
==================

First install gunicorn inside your virtual environment:

```
# as django
pip install -r requirements/gunicorn.txt
```

Systemd will launch the Gunicorn process on startup and keep running. Create a new systemd service file in `/etc/systemd/system/chatter_bot.service` and enter (you will need root/sudo permissions for that):

```
[Unit]
Description=Django gunicorn daemon
After=network.target

[Service]
User=django
Group=django
WorkingDirectory=/srv/django/chatter_bot
ExecStart=/srv/django/env/bin/gunicorn --bind unix:/srv/django/chatter_bot.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

This service needs to be started and enabled like any other service:

```
# as root
systemctl daemon-reload
systemctl start chatter_bot
systemctl enable chatter_bot
```

Next, install NGINX:


```
sudo apt install nginx  # on Debian/Ubuntu
sudo yum install nginx  # on RHEL/CentOS
```

Edit the Nginx configuration as follows (again with root/sudo permissions):

```
# in /etc/nginx/sites-available/default  on Debian/Ubuntu
# in /etc/nginx/conf.d/vhost.conf        on RHEL/CentOS
server {
    listen 80;
    server_name YOURDOMAIN;

    location / {
        proxy_pass http://unix:/srv/django/chatter_bot.sock;
    }
    location /static/ {
        alias /srv/django/chatter_bot/static_root/;
    }
}
```

Restart Nginx. The application should now be available on YOURDOMAIN. Note that the unix socket needs to be accessible by NGINX.

As you can see from the virtual host configurations, the static assets such as CSS and JavaScript files are served independently from the reverse proxy to the gunicorn process. In order to do so they need to be gathered in the `static_root` directory. This can be achieved by running:

```bash
python manage.py collectstatic
```

in your virtual environment.

In order to apply changes to the code, the Gunicorn process needs to be restarted:

```
sudo systemctl restart chatter_bot
```
