#!/bin/bash
set -e

python manage.py collectstatic --noinput --clear
echo -e "\nCollected static files"

python manage.py createcachetable
python manage.py makemigrations
python manage.py migrate
gunicorn -c config/gunicorn.conf.py thedevhunt.wsgi:application 
