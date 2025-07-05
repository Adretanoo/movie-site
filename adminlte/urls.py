from django.urls import path
from . import views

urlpatterns= [
    path('statistics/',views.statistics, name='statistics'),
    path('banners-sliders/',views.banners_sliders, name='banners-sliders'),
    path('movies/',views.movies, name='movies'),
    path('cinemas/',views.cinemas, name='cinemas'),
    path('news',views.news, name='news'),
    path('shares/',views.shares, name='shares'),
    path('pages/',views.pages, name='pages'),
    path('users/',views.users, name='users'),
    path('mailing/',views.mailing, name='mailing')

]