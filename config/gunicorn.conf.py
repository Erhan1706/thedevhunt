import os

# Create logs directory if it doesn't exist
log_path = "/home/django/thedevhunt/logs"
os.makedirs(log_path, exist_ok=True)

bind = "unix:/home/django/thedevhunt/thedevhunt.sock"
acesslog = "/home/django/thedevhunt/logs/gunicorn-access.log"
errorlog = "/home/django/thedevhunt/logs/gunicorn-error.log"
loglevel = "info"

workers = 3
worker_class = 'gstreamer'

wsgi_app = 'thedevhunt.wsgi:application'
proc_name = 'thedevhunt'

# Additional settings
timeout = 30
keepalive = 2