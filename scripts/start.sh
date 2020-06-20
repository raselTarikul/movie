#!/bin/bash

cd /opt/app/src/
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000