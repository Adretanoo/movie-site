from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from adminlte.models import Movie


class Command(BaseCommand):


    def handle(self, *args, **options):
        User = get_user_model()


        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@gmail.com', '1234')

        if not Movie.objects.exists():
            fixtures = [
                'store/adminlte_data.json',
                'store/seo_movie.json',
                'store/movies.json',
                'store/seats.json',
                'store/sessions.json',
                'store/template_mailin.json',
                'store/users.json',
            ]
            for fixture in fixtures:
                call_command('loaddata', fixture)

