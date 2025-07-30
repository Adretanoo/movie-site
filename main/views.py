from datetime import date

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.utils.safestring import mark_safe

from adminlte.models import MainPage, TopBanner, TopBannerImage, BackgroundBanner, BackgroundType, Movie, NewsBanner, \
    NewsBannerImage, Publication, PublicationType, PublicationGallery


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
        'bg_type': BackgroundType,
        'movie_today': movie_today,
        'movie_soon': movie_soon,
        'news_banner': news_banner,
        'news_banner_images': news_banner_images,
        'news_pages': news_pages,
    }
    return render(request, 'main/page/index.html', context)


def shares_page(request):
    seo_page = [{
        'title': 'Акции',
        'keywords': 'dsfja',
        'description': 'text'
    }]
    return shares_news_page(request, PublicationType.SHARES, seo_page)


def news_page(request):
    seo_page = [{
        'title': 'Новини',
        'keywords': 'dsfja',
        'description': 'text'
    }]
    return shares_news_page(request, PublicationType.NEWS, seo_page)


def about_page(request):
    return publication_page(request, PublicationType.ABOUT)


def cafe_bar_page(request):
    return publication_page(request, PublicationType.CAFE_BAR)


def vip_hall_page(request):
    return publication_page(request, PublicationType.VIP_HALL)


def advertising_page(request):
    return publication_page(request, PublicationType.ADVERTISING)


def children_room_page(request):
    return publication_page(request, PublicationType.CHILDREN_ROOM)


def shares_news_page(request, publication_type, seo_global_page):

    pub_list = Publication.objects.filter(publication_type=publication_type, is_enabled=True)

    top_banner = TopBanner.objects.first()
    top_banner_images = TopBannerImage.objects.all()

    paginator = Paginator(pub_list, 3)
    page = request.GET.get('page')

    try:
        pub = paginator.page(page)
    except PageNotAnInteger:
        pub = paginator.page(1)
    except EmptyPage:
        pub = paginator.page(paginator.num_pages)

    context = {
        'pub': pub,
        'seo_global_page': seo_global_page,
        'top_banner': top_banner,
        'top_banner_images': top_banner_images,
        'pub_type': PublicationType,
        'publication_type': publication_type,
    }
    return render(request, 'main/page/base_shares_news.html', context)


def shares_card(request, pk):
    return shares_news_card(request, PublicationType.SHARES, pk)


def news_card(request, pk):
    return shares_news_card(request, PublicationType.NEWS, pk)


def shares_news_card(request, publication_type, pk):
    try:
        pub = Publication.objects.get(pk=pk)
    except Publication.DoesNotExist:
        pub = None

    gallery = PublicationGallery.objects.filter(publication=pub).select_related('image')

    top_banner = TopBanner.objects.first()
    top_banner_images = TopBannerImage.objects.all()

    video_html = f'''
            <div class="video-wrapper my-4">
                    <iframe width="100%" height="515"
                        src="{pub.video_url}"
                        title="Відео"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen>
                    </iframe>
                </div>
            '''
    desc_with_breaks = pub.description.replace('\n', '<br>')
    desc_format = desc_with_breaks.replace('[VIDEO]', video_html)

    context = {
        'pub': pub,
        'top_banner': top_banner,
        'top_banner_images': top_banner_images,
        'pub_type': PublicationType,
        'publication_type': publication_type,
        'desc_with_video': desc_format,
        'gallery': gallery,
    }
    return render(request, 'main/page/base_shares_news_card.html', context)


def publication_page(request, publication_type):
    pub = Publication.objects.get(publication_type=publication_type)
    gallery = PublicationGallery.objects.filter(publication=pub).select_related('image')

    video_html = f'''
        <div class="video-wrapper my-4">
                <iframe width="100%" height="515"
                    src="{pub.video_url}"
                    title="Відео"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
                </iframe>
            </div>
        '''

    desc_with_breaks = pub.description.replace('\n', '<br>')
    desc_format = desc_with_breaks.replace('[VIDEO]', video_html)
    context = {
        'publication': pub,
        'desc_with_video': desc_format,
        'gallery': gallery,
    }
    return render(request, 'main/page/base_publication.html', context)
