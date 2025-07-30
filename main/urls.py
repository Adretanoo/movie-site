from django.urls import path

from main import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about_page, name='about_page'),
    path('cafe-bar/', views.cafe_bar_page, name='cafe_bar_page'),
    path('vip-hall/', views.vip_hall_page, name='vip_hall_page'),
    path('advertising/', views.advertising_page, name='advertising_page'),
    path('children-room/', views.children_room_page, name='children_room_page'),

    path('shares/', views.shares_page, name='shares_page'),
    path('news/', views.news_page, name='news_page'),

    path('shares/card/<int:pk>/',views.shares_card, name='shares_card'),
    path('news/card/<int:pk>/',views.news_card, name='news_card'),
]
