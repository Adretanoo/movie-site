import django_filters
from django.db.models.functions.datetime import TruncDate
from django_filters import FilterSet, ChoiceFilter


from adminlte.models import Movie, CardCinema, CardHall
from .models import Session



class SessionFilter(django_filters.FilterSet):
    start_time = ChoiceFilter(
        choices=lambda: [
            (date, date.strftime('%Y-%m-%d')) for date in
            Session.objects.annotate(
                date_only=TruncDate('start_time')
            ).values_list('date_only', flat=True).distinct()
        ],
        empty_label='Дата',
        method='filter_by_date'
    )
    is_3d = django_filters.BooleanFilter(
        field_name='movie__is_3d',
        label='is_3d',
    )
    is_2d = django_filters.BooleanFilter(
        field_name='movie__is_2d',
        label='is_2d',
    )
    is_imax = django_filters.BooleanFilter(
        field_name='movie__is_imax',
        label='is_imax',
    )

    movie = django_filters.ModelChoiceFilter(queryset=Movie.objects.all(), empty_label='Фильм: все')
    card_hall = django_filters.ModelChoiceFilter(queryset=CardHall.objects.all(), empty_label='Зал: все')
    cinema = django_filters.ModelChoiceFilter(queryset=CardCinema.objects.all(), field_name='card_hall__card_cinema',
                                              empty_label='Кинотеатр')

    class Meta:
        model = Session
        fields = ['start_time', 'movie', 'card_hall', 'cinema']

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(start_time__date=value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_cinema_pk = self.data.get('cinema')

        if selected_cinema_pk:
            halls_queryset = CardHall.objects.filter(card_cinema__pk=selected_cinema_pk)
            self.filters['card_hall'].queryset = halls_queryset
