#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
python manage.py makemigrations endpoint
python manage.py migrate
# python manage.py collectstatic --no-input
python manage.py ensure_adminuser --username=aa \
    --email=test@test.com \
    --password=123123

exec "$@"
