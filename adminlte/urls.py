from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('statistics/', views.statistics, name='statistics'),
    path('banners-sliders/', views.banners_sliders, name='banners-sliders'),
    path('movies/', views.movies, name='movies'),
    path('cinemas/', views.cinemas, name='cinemas'),
    path('news/', views.news, name='news'),
    path('shares/', views.shares, name='shares'),
    path('pages/', views.pages, name='pages'),
    path('users/', views.users, name='users'),
    path('mailing/', views.mailing, name='mailing'),

    path('banners-sliders/add/', views.banners_sliders_add, name='banners-sliders-add'),

    path('movie/add/', views.movie_add, name='movie_add'),

    path('news/add/', views.news_add, name='add_news'),
    path('news/delete/<int:pk>/', views.delete_news, name='delete_news'),
    path('news/edit/<int:pk>/', views.edit_news, name='edit_news'),

    path("news/delete/<int:pk>/", views.delete_publication, name="delete_publication"),

    path('shares/add/', views.shares_add, name='add_shares'),
    path('shares/delete/<int:pk>/', views.shares_delete, name='delete_shares'),
    path('shares/edit/<int:pk>/', views.shares_edit, name='edit_shares'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
