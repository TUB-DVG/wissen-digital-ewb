#!/bin/sh

set -e
cd /src/01_application/webcentral_app
#python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module webcentral_app.wsgi

