from datetime import date, datetime

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions.datetime import TruncDate
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from poetry.puzzle import transaction

from adminlte.models import MainPage, TopBanner, TopBannerImage, BackgroundBanner, BackgroundType, Movie, NewsBanner, \
    NewsBannerImage, Publication, PublicationType, PublicationGallery, ContactsPage, ContactsPageLocation, CardCinema, \
    CardCinemaGallery, CardHall, CardHallGallery
from main.models import Session
from user.forms import UserRegisterForm, UserEditProfileForm
from user.models import User

import django_filters

from .filters import SessionFilter
from .models import Session


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
    publication = Publication.objects.all()

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
        'menu_pub': publication,
        'pub_type': PublicationType,
    }
    return render(request, 'main/page/index.html', context)




def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('user_profile', username=user.username)
    else:
        form = UserRegisterForm()

    return render(request, 'main/page/register.html', {'form': form})


def cinemas_page(request):
    cinemas = CardCinema.objects.all()
    top_banner = TopBanner.objects.first()
    top_banner_images = TopBannerImage.objects.all()

    context = {
        'cinemas': cinemas,
        'top_banner': top_banner,
        'top_banner_images': top_banner_images,

    }
    return render(request, 'main/page/cinemas.html', context)


def cinema_card_page(request, pk):
    cinema = CardCinema.objects.get(pk=pk)
    cinema_gallery_card = CardCinemaGallery.objects.filter(card_cinema=cinema.pk)
    cinema_halls = CardHall.objects.filter(card_cinema=cinema.pk)

    today_date = datetime.now().date()

    sessions = Session.objects.select_related('movie', 'card_hall__card_cinema').filter(card_hall__card_cinema=cinema,
                                                                                        start_time__date=today_date).order_by(
        'start_time')
    halls_count = len(cinema_halls)

    context = {
        'cinema': cinema,
        'cinema_gallery_card': cinema_gallery_card,
        'cinema_halls': cinema_halls,
        'halls_count': halls_count,
        'sessions': sessions,
        'today_date': today_date,
    }
    return render(request, 'main/page/cinema_card.html', context)


def hall_card_page(request, pk, hall_index):
    halls = CardHall.objects.filter(card_cinema=pk).order_by('id')
    hall = halls[hall_index]

    hall_gallery = CardHallGallery.objects.filter(card_hall=hall)

    sessions = Session.objects.select_related('movie', 'card_hall__card_cinema').filter(card_hall__card_cinema=pk,card_hall=hall,
                                                                                        start_time__date=datetime.now().date()).order_by('start_time')

    context = {
        'hall': hall,
        'hall_gallery': hall_gallery,
        'lang': request.LANGUAGE_CODE,
        'sessions': sessions,
    }
    return render(request, 'main/page/hall_card.html', context)


def schedule(request):
    sessions = Session.objects.select_related('movie', 'card_hall', 'card_hall__card_cinema').all()
    f = SessionFilter(request.GET, queryset=sessions)

    unique_data_sessions = f.qs.filter(
        start_time__gte=datetime.now().date()
    ).annotate(
        data_only=TruncDate('start_time')).values_list('data_only', flat=True).distinct()
    context = {
        'filter': f,
        'sessions': f.qs,
        'unique_data_sessions': unique_data_sessions,
    }
    return render(request, 'main/page/schedule.html', context)


@login_required
def user_edit_profile(request, username):
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = UserEditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            if form.cleaned_data.get('new_password1'):
                update_session_auth_hash(request, user)
            return redirect('user_profile', username=user.username)
    else:
        form = UserEditProfileForm(instance=user)

    return render(request, 'main/page/edit_profile_user.html', context={'form': form})


@login_required(login_url='login')
def user_profile(request, username):
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    return render(request, 'main/accounts/user_profile.html')


def shares_page(request):
    seo_page = [{
        'title': 'Акции',
        'keywords': 'акции,лутшие акции',
        'description': 'text'
    }]
    return shares_news_page(request, PublicationType.SHARES, seo_page)


def news_page(request):
    seo_page = [{
        'title': 'Новости',
        'keywords': 'новости,лутшие новости',
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

    news_pages = Publication.objects.filter(publication_type=PublicationType.NEW_PAGE)
    context = {
        'pub': pub,
        'seo_global_page': seo_global_page,
        'top_banner': top_banner,
        'top_banner_images': top_banner_images,
        'pub_type': PublicationType,
        'publication_type': publication_type,
        'news_pages': news_pages,
    }
    return render(request, 'main/page/base_shares_news.html', context)


def shares_card(request, pk):
    return shares_news_card(request, PublicationType.SHARES, pk)


def news_card(request, pk):
    return shares_news_card(request, PublicationType.NEWS, pk)


def contact_page(request):
    contacts_seo = ContactsPage.objects.first()
    contacts = ContactsPageLocation.objects.all()

    top_banner = TopBanner.objects.first()
    top_banner_images = TopBannerImage.objects.all()
    news_pages = Publication.objects.filter(publication_type=PublicationType.NEW_PAGE)

    context = {
        'contacts_seo': contacts_seo,
        'contacts': contacts,
        'top_banner': top_banner,
        'top_banner_images': top_banner_images,
        'news_pages': news_pages,
    }
    return render(request, 'main/page/contacts.html', context)


def new_page(request, pk):
    pub = Publication.objects.get(publication_type=PublicationType.NEW_PAGE, pk=pk)
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
    news_pages = Publication.objects.filter(publication_type=PublicationType.NEW_PAGE)

    context = {
        'publication': pub,
        'desc_with_video': desc_format,
        'gallery': gallery,
        'news_pages': news_pages,
    }
    return render(request, 'main/page/new_page.html', context)


def shares_news_card(request, publication_type, pk):
    try:
        pub = Publication.objects.get(pk=pk)
    except Publication.DoesNotExist:
        pub = None

    gallery = PublicationGallery.objects.filter(publication=pub).select_related('image')

    top_banner = TopBanner.objects.first()
    top_banner_images = TopBannerImage.objects.all()
    news_pages = Publication.objects.filter(publication_type=PublicationType.NEW_PAGE)
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
        'news_pages': news_pages,
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
    news_pages = Publication.objects.filter(publication_type=PublicationType.NEW_PAGE)
    context = {
        'publication': pub,
        'desc_with_video': desc_format,
        'gallery': gallery,
        'news_pages': news_pages,
        'pub_type': PublicationType,
        'publication_type': publication_type,
    }
    return render(request, 'main/page/base_publication.html', context)
