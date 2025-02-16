#!/bin/bash
set -e

python manage.py collectstatic --noinput --clear
echo -e "\nCollected static files"

python manage.py migrate
gunicorn --bind 0.0.0.0:8000 thedevhunt.wsgi:application --workers=4
