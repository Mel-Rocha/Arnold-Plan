#!/bin/bash

echo "Apply database migrations"
python3 manage.py migrate

echo "Collect static files"
python3 manage.py collectstatic --noinput

# Executing test case
#echo "Executing test case"
#python3 manage.py test

# Start application
echo "Start application"
gunicorn config.wsgi:application -c gunicorn_config.py

exec "$@"