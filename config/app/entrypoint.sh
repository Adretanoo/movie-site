#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate --noinput

python manage.py loaddata store/adminlte_data.json
python manage.py loaddata store/seo_movie.json
python manage.py loaddata store/movies.json
python manage.py loaddata store/seats.json
python manage.py loaddata store/sessions.json
python manage.py loaddata store/template_mailin.json
python manage.py loaddata store/users.json

python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@gmail.com', '1234')"

exec "$@"
