#!/bin/sh

echo "Starting django in 5 seconds..."
sleep 5

python manage.py migrate
python manage.py runserver 0.0.0.0:8000