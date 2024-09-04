#!/bin/bash
set -e

./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
echo -e "\nCompiled tailwind"

python manage.py collectstatic
echo -e "\nCollected static files"

python manage.py makemigrations
python manage.py migrate

mkdir logs
