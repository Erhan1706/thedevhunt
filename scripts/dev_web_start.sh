#!/bin/bash
set -e

#python manage.py collectstatic
#echo -e "\nCollected static files"

python manage.py migrate
#python manage.py runserver 0.0.0.0:8000
python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
#python -m debugpy --listen 0.0.0.0:5678 --wait-for-client manage.py fetch_jobs 