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
    {'title': 'Рассылка', 'url_name': 'newsletter', 'icon': 'fa-envelope'},
]


def statistics(request):
    return render(request, "adminlte/pages/statistics.html", context={'menu': menu})


def banners_sliders(request):
    return HttpResponse("<UNK>")


def movies(request):
    return HttpResponse("<UNK>")


def cinemas(request):
    return HttpResponse("<UNK>")


def news(request):
    return HttpResponse("<UNK>")


def shares(request):
    return HttpResponse("<UNK>")


def pages(request):
    return HttpResponse("<UNK>")


def users(request):
    return HttpResponse("<UNK>")


def newsletter(request):
    return HttpResponse("<UNK>")
