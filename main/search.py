from datetime import date, datetime

from django.db.models.functions.datetime import TruncDate
from django.views.generic.list import ListView

from adminlte.models import Movie, CardCinema, Publication, PublicationType
from main.filters import SessionFilter
from main.models import Session


class SearchMain(ListView):
    template_name = 'main/page/index.html'
    context_object_name = 'movie_today'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class SearchPoster(ListView):
    template_name = 'main/page/poster.html'
    context_object_name = 'movies'

    def get_queryset(self):
        movies = Session.objects.select_related('movie').filter(movie__title__icontains=self.request.GET.get('q'))
        return movies.distinct('movie')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class SearchCinema(ListView):
    template_name = 'main/page/cinemas.html'
    context_object_name = 'cinemas'

    def get_queryset(self):
        return CardCinema.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class SearchSchedule(ListView):
    template_name = 'main/page/schedule.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        self.q = self.request.GET.get('q', '').strip()
        queryset = Session.objects.select_related('movie', 'card_hall', 'card_hall__card_cinema')
        if self.q:
            queryset = queryset.filter(movie__title__icontains=self.q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        f = SessionFilter(self.request.GET, queryset=self.object_list)

        unique_data_sessions = f.qs.filter(
            start_time__gte=datetime.now().date()
        ).annotate(
            data_only=TruncDate('start_time')
        ).values_list('data_only', flat=True).distinct()

        context['filter'] = f
        context['unique_data_sessions'] = unique_data_sessions
        context['q'] = self.q
        context['sessions'] = f.qs

        return context


class SearchShares(ListView):
    template_name = 'main/page/base_shares_news.html'
    context_object_name = 'pub'

    def get_queryset(self):
        return Publication.objects.filter(publication_type=PublicationType.SHARES,title__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['publication_type'] = PublicationType.SHARES
        return context

class SearchNews(ListView):
    template_name = 'main/page/base_shares_news.html'
    context_object_name = 'pub'

    def get_queryset(self):
        return Publication.objects.filter(publication_type=PublicationType.NEWS,title__icontains=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['publication_type'] = PublicationType.NEWS
        return context
