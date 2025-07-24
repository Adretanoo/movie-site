from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import UsersAjaxDataTable

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

    path('cinemas/add', views.cinemas_add, name='cinemas_add'),
    path('cinemas/edit/<int:pk>', views.cinemas_edit, name='cinemas_edit'),
    path('cinemas/delete/', views.cinemas_delete, name='cinemas_delete'),
    path('hall/add', views.hall_add, name='hall_add'),
    path('hall/edit/<int:pk>', views.hall_edit, name='hall_edit'),
    path('hall/delete/<int:pk>/', views.hall_delete, name='hall_delete'),

    path('movie/add/', views.movie_add, name='movie_add'),
    path('movie/edit/<int:pk>/', views.movie_edit, name='movie_edit'),
    path('movie/delete/', views.movies_delete, name='movie_delete'),

    path('news/add/', views.news_add, name='add_news'),
    path('news/delete/<int:pk>/', views.delete_news, name='delete_news'),
    path('news/edit/<int:pk>/', views.edit_news, name='edit_news'),

    path("news/delete/<int:pk>/", views.delete_publication, name="delete_publication"),

    path('shares/add/', views.shares_add, name='add_shares'),
    path('shares/delete/<int:pk>/', views.shares_delete, name='delete_shares'),
    path('shares/edit/<int:pk>/', views.shares_edit, name='edit_shares'),

    path('pages/about/', views.about, name='about'),
    path('pages/cafe-bar/', views.cafe_bar, name='cafe_bar'),
    path('pages/vip-hall/', views.vip_hall, name='vip_hall'),
    path('pages/advertising/', views.advertising, name='advertising'),
    path('pages/children-room/', views.children_room, name='children_room'),
    path('pages/main-page/', views.main_page, name='main_page'),
    path('pages/contacts-page/', views.contacts_page, name='contacts_page'),
    path('pages/new-page/add/', views.new_page_add, name='new_page_add'),
    path('pages/new-page/edit/<int:pk>/', views.new_page_edit, name='new_page_edit'),
    path('pages/new-page/delete/<int:pk>', views.new_page_delete, name='new_page_delete'),

    path('users-data/', UsersAjaxDataTable.as_view(), name='ajax_datatable_users'),

    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('users/delete/', views.user_delete, name='user_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
