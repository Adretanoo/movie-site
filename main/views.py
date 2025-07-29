
from datetime import date

from django.shortcuts import render
from adminlte.models import MainPage, TopBanner, TopBannerImage, BackgroundBanner, BackgroundType, Movie, NewsBanner, \
    NewsBannerImage, Publication, PublicationType


def main(request):
    main_page = MainPage.objects.first()
    top_banner = TopBanner.objects.first()
    top_banner_images = TopBannerImage.objects.all()
    bg_banner = BackgroundBanner.objects.first()

    movie_today = Movie.objects.filter(published_at__date=date.today())
    movie_soon = Movie.objects.filter(published_at__date__gt=date.today())
    news_banner = NewsBanner.objects.first()
    news_banner_images = NewsBannerImage.objects.all()

    news_pages = Publication.objects.filter(publication_type=PublicationType.NEW_PAGE)
    print(news_pages)



    context = {
        'main_page': main_page,
        'top_banner': top_banner,
        'top_banner_images': top_banner_images,
        'bg_banner': bg_banner,
        'bg_type':BackgroundType,
        'movie_today': movie_today,
        'movie_soon': movie_soon,
        'news_banner': news_banner,
        'news_banner_images': news_banner_images,
        'news_pages': news_pages,
    }
    return render(request, 'main/page/index.html',context)
