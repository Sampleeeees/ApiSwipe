#!/bin/sh

if [ "$DATABASE" = 'postgres' ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py collectstatic --no-input --clear
python manage.py makemigrations
python manage.py migrate
python manage.py create_role
python manage.py create_user
python manage.py house_create
python manage.py create_favorite
python manage.py create_promotion
python manage.py create_message

exec "$@"