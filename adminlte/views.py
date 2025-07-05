from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

menu = [
    {'title': 'Статистика', 'url_name': 'statistics', 'icon': 'fa-chart-line'},
    {'title': 'Баннера/Слайдеры', 'url_name': 'banners-sliders', 'icon': 'fa-image'},
    {'title': 'Фильмы', 'url_name': 'movies', 'icon': 'fa-film'},
    {'title': 'Кинотеатры', 'url_name': 'cinemas', 'icon': 'fa-building'},
    {'title': 'Новости', 'url_name': 'news', 'icon': 'fa-newspaper'},
    {'title': 'Акции', 'url_name': 'shares', 'icon': 'fa-tags'},
    {'title': 'Страницы', 'url_name': 'pages', 'icon': 'fa-file-alt'},
    {'title': 'Пользователи', 'url_name': 'users', 'icon': 'fa-users'},
    {'title': 'Рассылка', 'url_name': 'mailing', 'icon': 'fa-envelope'},
]


def statistics(request):
    return render(request, "adminlte/pages/statistics.html", context={'menu': menu})


def banners_sliders(request):
    return render(request, 'adminlte/pages/banners_sliders_table.html', context={'menu': menu})


def movies(request):
    return render(request, 'adminlte/pages/movies_table.html', context={'menu': menu})


def cinemas(request):
    return render(request, 'adminlte/pages/cinemas_table.html', context={'menu': menu})


def news(request):
    return render(request, 'adminlte/pages/news_table.html', context={'menu': menu})


def shares(request):
    return render(request, 'adminlte/pages/shares_table.html', context={'menu': menu})


def pages(request):
    return render(request, 'adminlte/pages/pages_table.html', context={'menu': menu})


def users(request):
    return render(request, 'adminlte/pages/users_table.html', context={'menu': menu})


def mailing(request):
    return render(request, 'adminlte/pages/mailing.html', context={'menu': menu})
