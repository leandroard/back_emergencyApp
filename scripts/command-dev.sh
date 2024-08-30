#!/bin/sh

python manage.py migrate
python manage.py loaddata dev --verbosity 2
python manage.py runserver 0.0.0.0:8000