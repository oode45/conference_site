#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py makemigrations news
python manage.py makemigrations about_conf
python manage.py makemigrations archive
python manage.py makemigrations faq
python manage.py makemigrations participant_registration
python manage.py makemigrations photogallery
python manage.py migrate
exec "$@"
