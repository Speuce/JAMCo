#!/bin/sh

echo "Starting django in 5 seconds..."
sleep 5

python backend/manage.py migrate
python backend/manage.py runserver 0.0.0.0:8000