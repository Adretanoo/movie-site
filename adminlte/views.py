import datetime

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from adminlte.models import Publication, Images, PublicationType, TopBanner, NewsBanner, BackgroundBanner, \
    TopBannerImage, NewsBannerImage, Movie, MovieGallery, SeoMetadata, CardCinema, CardHall, MainPage, ContactsPage
from .forms import PublicationForm, SeoMetadataForm, BackgroundBannerForm, TopBannerForm, TopBannerImageForm, \
    TopBannerImageFormSet, NewsBannerForm, NewsBannerImageFormSet, MovieForm, MovieGalleryFormSet, CardCinemaForm, \
    CardCinemaGalleryFormSet, CardHallForm, CardHallGalleryForm, CardHallGalleryFormSet, PublicationGalleryFormSet, \
    MainPageForm
from django.shortcuts import render, redirect
from cinemasite.settings import menu


def statistics(request):
    return render(request, "adminlte/pages/statistics.html", context={'menu': menu})


def banners_sliders(request):
    bg_banner = BackgroundBanner.objects.first()

    top_banner_image = TopBannerImage.objects.first()
    top_banner = None
    if top_banner_image and top_banner_image.image_id:
        top_banner = Images.objects.filter(id=top_banner_image.image_id).first()

    news_banner_image = NewsBannerImage.objects.first()
    news_banner = None
    if news_banner_image and news_banner_image.image_id:
        news_banner = Images.objects.filter(id=news_banner_image.image_id).first()

    context = {
        'bg_banner': bg_banner,
        'menu': menu,
        'top_banner': top_banner,
        'news_banner': news_banner,
    }
    return render(request, 'adminlte/pages/banners_sliders_display.html', context)


def banners_sliders_add(request):
    top_banner_instance, _ = TopBanner.objects.get_or_create(id=1)
    news_banner_instance, _ = NewsBanner.objects.get_or_create(id=1)

    bg_instance = BackgroundBanner.objects.first()
    if not bg_instance:
        bg_instance = BackgroundBanner()

    top_form = TopBannerForm(instance=top_banner_instance)
    news_form = NewsBannerForm(instance=news_banner_instance)
    background_form = BackgroundBannerForm(instance=bg_instance)

    top_image_formset = TopBannerImageFormSet(instance=top_banner_instance, prefix='topbannerimage_set')
    news_image_formset = NewsBannerImageFormSet(instance=news_banner_instance, prefix='newsbannerimage_set')

    if request.method == "POST":
        if 'submit_upper_banners' in request.POST:
            top_form = TopBannerForm(request.POST, request.FILES, instance=top_banner_instance)
            top_image_formset = TopBannerImageFormSet(
                request.POST,
                request.FILES,
                instance=top_banner_instance,
                prefix='topbannerimage_set'
            )

            if top_form.is_valid():
                with transaction.atomic():
                    top_form.save()
                    for form in top_image_formset.forms:
                        if form.is_valid():
                            if not form.cleaned_data.get('DELETE', False):
                                form.save()
                        elif form.cleaned_data.get('DELETE', False) and form.instance.pk:
                            if form.instance.image:
                                form.instance.image.delete()
                            form.instance.delete()
                return redirect('banners-sliders-add')

        elif 'submit_background_banner' in request.POST:
            background_form = BackgroundBannerForm(request.POST, request.FILES, instance=bg_instance)
            if background_form.is_valid():
                background_form.save()
                return redirect('banners-sliders-add')

        elif 'submit_news_banners' in request.POST:
            news_form = NewsBannerForm(request.POST, request.FILES, instance=news_banner_instance)
            news_image_formset = NewsBannerImageFormSet(
                request.POST,
                request.FILES,
                instance=news_banner_instance,
                prefix='newsbannerimage_set'
            )

            if news_form.is_valid():
                with transaction.atomic():
                    news_form.save()
                    for form in news_image_formset.forms:
                        if form.is_valid():
                            if not form.cleaned_data.get('DELETE', False):
                                form.save()
                        elif form.cleaned_data.get('DELETE', False) and form.instance.pk:
                            if form.instance.image:
                                form.instance.image.delete()
                            form.instance.delete()
                return redirect('banners-sliders-add')

    context = {
        'menu': menu,
        'bg_form': background_form,
        'top_form': top_form,
        'top_image_formset': top_image_formset,
        'news_form': news_form,
        'news_image_formset': news_image_formset,
        'bg_instance': bg_instance,
    }
    return render(request, 'adminlte/pages/add/banners_sliders_full.html', context)


def movies(request):
    current_data = datetime.datetime.now()

    current_movies = Movie.objects.filter(published_at=format(current_data, '%Y-%m-%d'))
    soon_movies = Movie.objects.filter(published_at__gt=format(current_data, '%Y-%m-%d'))
    list_movies = Movie.objects.all()

    context = {
        'menu': menu,
        'current_movies': current_movies,
        'soon_movies': soon_movies,
        'list_movies': list_movies,
    }
    return render(request, 'adminlte/pages/movies_display.html', context)


def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    seo = get_object_or_404(SeoMetadata, pk=movie.seo_id)
    lang = request.GET.get('lang', 'ru')

    if request.method == 'POST':
        main_form = MovieForm(request.POST, request.FILES, instance=movie, prefix='main')
        seo_form = SeoMetadataForm(request.POST, instance=seo, prefix='seo')
        formset = MovieGalleryFormSet(request.POST, request.FILES, instance=movie, prefix='basegallery_set')

        if main_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                movie_instance = main_form.save(commit=False)
                movie_instance.seo = seo_instance
                movie_instance.save()

                formset.instance = movie_instance
                formset.save()

            messages.success(request, 'Фільм успішно оновлено!')
            return redirect('movies')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        main_form = MovieForm(instance=movie, prefix='main')
        seo_form = SeoMetadataForm(instance=seo, prefix='seo')
        formset = MovieGalleryFormSet(instance=movie, prefix='basegallery_set')

    context = {
        'menu': menu,
        'form': main_form,
        'seo_form': seo_form,
        'formset': formset,
        'lang': lang,
        'movie': movie
    }
    return render(request, 'adminlte/pages/edit/movies_edit.html', context)


@require_POST
def movies_delete(request):
    movie_id = request.POST.get('movie_id')
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('movies')


def movie_add(request):
    lang = request.GET.get('lang', 'ru')

    if request.method == 'POST':
        main_form = MovieForm(request.POST, request.FILES, prefix='main')
        seo_form = SeoMetadataForm(request.POST, prefix='seo')
        formset = MovieGalleryFormSet(request.POST, request.FILES, prefix='basegallery_set')

        if main_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                movie_instance = main_form.save(commit=False)
                movie_instance.seo = seo_instance
                movie_instance.save()

                formset.instance = movie_instance
                formset.save()

            messages.success(request, 'Фільм успішно додано!')
            return redirect('movies')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        main_form = MovieForm(prefix='main')
        seo_form = SeoMetadataForm(prefix='seo')
        formset = MovieGalleryFormSet(prefix='basegallery_set')

    context = {
        'menu': menu,
        'lang': lang,
        'form': main_form,
        'seo_form': seo_form,
        'formset': formset,
    }
    return render(request, 'adminlte/pages/add/movie_add.html', context)


def cinemas(request):
    cinema = CardCinema.objects.all()
    context = {
        'menu': menu,
        'cinema': cinema,
    }
    return render(request, 'adminlte/pages/cinemas_display.html', context)


def cinemas_edit(request, pk):
    lang = request.GET.get('lang', 'ru')
    cinema = get_object_or_404(CardCinema, pk=pk)
    seo = get_object_or_404(SeoMetadata, pk=cinema.seo.pk)

    halls = CardHall.objects.filter(card_cinema=cinema)

    if request.method == 'POST':
        main_form = CardCinemaForm(request.POST, request.FILES, instance=cinema, prefix='main')
        seo_form = SeoMetadataForm(request.POST, instance=seo, prefix='seo')
        formset = CardCinemaGalleryFormSet(request.POST, request.FILES, instance=cinema, prefix='basegallery_set')

        if main_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                cinema_instance = main_form.save(commit=False)
                cinema_instance.seo = seo_instance
                cinema_instance.save()

                formset.instance = cinema_instance
                formset.save()

            return redirect('cinemas')
    else:
        main_form = CardCinemaForm(instance=cinema, prefix='main')
        seo_form = SeoMetadataForm(instance=seo, prefix='seo')
        formset = CardCinemaGalleryFormSet(instance=cinema, prefix='basegallery_set')
    context = {
        'menu': menu,
        'lang': lang,
        'cinema': cinema,
        'form': main_form,
        'seo_form': seo_form,
        'formset': formset,
        'halls': halls
    }
    return render(request, 'adminlte/pages/edit/cinema_edit.html', context)


def cinemas_add(request):
    lang = request.GET.get('lang', 'ru')

    if request.method == 'POST':
        main_form = CardCinemaForm(request.POST, request.FILES, prefix='main')
        formset = CardCinemaGalleryFormSet(request.POST, request.FILES, prefix='basegallery_set')
        seo_form = SeoMetadataForm(request.POST, prefix='seo')
        if main_form.is_valid() and formset.is_valid() and seo_form.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                cinema_instance = main_form.save(commit=False)
                cinema_instance.seo = seo_instance
                cinema_instance.save()

                formset.instance = cinema_instance
                formset.save()

            return redirect('cinemas')
    else:
        main_form = CardCinemaForm(prefix='main')
        seo_form = SeoMetadataForm(prefix='seo')
        formset = CardCinemaGalleryFormSet(prefix='basegallery_set')

    context = {
        'form': main_form,
        'formset': formset,
        'seo_form': seo_form,
        'menu': menu,
        'lang': lang,
    }
    return render(request, 'adminlte/pages/add/cinemas_add.html', context)


@require_POST
def cinemas_delete(request):
    cinema_id = request.POST.get('cinema_id')
    cinema = get_object_or_404(CardCinema, pk=cinema_id)
    cinema.delete()
    return redirect('cinemas')


def hall_add(request):
    lang = request.GET.get('lang', 'ru')
    cinema = get_object_or_404(CardCinema, pk=request.GET.get('cinema_id'))

    if request.method == 'POST':
        main_form = CardHallForm(request.POST, request.FILES, prefix='main')
        formset = CardHallGalleryFormSet(request.POST, request.FILES, prefix='basegallery_set')
        seo_form = SeoMetadataForm(request.POST, prefix='seo')
        if main_form.is_valid() and formset.is_valid() and seo_form.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()

                hall_instance = main_form.save(commit=False)
                hall_instance.seo = seo_instance
                hall_instance.card_cinema = cinema
                hall_instance.save()

                formset.instance = hall_instance
                formset.save()
            return redirect('cinemas_edit', pk=cinema.pk)
    else:
        main_form = CardHallForm(prefix='main')
        seo_form = SeoMetadataForm(prefix='seo')
        formset = CardCinemaGalleryFormSet(prefix='basegallery_set')

    context = {
        'menu': menu,
        'lang': lang,
        'cinema': cinema,
        'form': main_form,
        'formset': formset,
        'seo_form': seo_form,
    }
    return render(request, 'adminlte/pages/add/hall_add.html', context)


def hall_edit(request, pk):
    lang = request.GET.get('lang', 'ru')
    cinema = get_object_or_404(CardCinema, pk=request.GET.get('cinema_id'))
    hall = get_object_or_404(CardHall, pk=pk)
    seo = hall.seo

    if request.method == 'POST':
        main_form = CardHallForm(request.POST, request.FILES, prefix='main', instance=hall)
        seo_form = SeoMetadataForm(request.POST, prefix='seo', instance=seo)
        formset = CardHallGalleryFormSet(request.POST, request.FILES, prefix='basegallery_set', instance=hall)

        if main_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()

                hall_instance = main_form.save(commit=False)
                hall_instance.seo = seo_instance
                hall_instance.card_cinema = cinema
                hall_instance.save()

                formset.instance = hall_instance
                formset.save()
            return redirect('cinemas_edit', pk=cinema.pk)

    else:
        main_form = CardHallForm(prefix='main', instance=hall)
        seo_form = SeoMetadataForm(prefix='seo', instance=seo)
        formset = CardHallGalleryFormSet(prefix='basegallery_set', instance=hall)

    context = {
        'menu': menu,
        'lang': lang,
        'cinema': cinema,
        'form': main_form,
        'formset': formset,
        'seo_form': seo_form,
    }
    return render(request, 'adminlte/pages/edit/hall_edit.html', context)


@require_POST
def hall_delete(request, pk):
    hall = get_object_or_404(CardHall, pk=pk)
    cinema_pk = hall.card_cinema.pk
    hall.delete()
    return redirect('cinemas_edit', pk=cinema_pk)


def news(request):
    publications = Publication.objects.filter(publication_type=PublicationType.NEWS)
    return render(request, 'adminlte/pages/news_tabel.html', context={'menu': menu, 'publications': publications})


def news_add(request):
    return add_publication(
        request=request,
        publication_type=PublicationType.NEWS,
        template_name='adminlte/pages/add/base_add.html',
        redirect_url='news'
    )


def edit_news(request, pk):
    return edit_publication(
        request=request,
        pk=pk,
        publication_type=PublicationType.NEWS,
        template_name='adminlte/pages/edit/base_edit.html',
        redirect_url='news'
    )


def shares_delete(request, pk):
    return delete_publication(
        request=request,
        pk=pk,
    )


def delete_news(request, pk):
    return delete_publication(
        request=request,
        pk=pk,
    )


def shares(request):
    publications = Publication.objects.filter(publication_type=PublicationType.SHARES)
    return render(request, 'adminlte/pages/shares_table.html', context={'menu': menu, 'publications': publications})


def shares_add(request):
    return add_publication(
        request=request,
        publication_type=PublicationType.SHARES,
        template_name='adminlte/pages/add/base_add.html',
        redirect_url='shares'
    )


def shares_edit(request, pk):
    return edit_publication(
        request=request,
        pk=pk,
        publication_type=PublicationType.SHARES,
        template_name='adminlte/pages/edit/base_edit.html',
        redirect_url='shares'
    )


def pages(request):
    publications = [
        {'name': 'Главная страница', 'obj': MainPage.objects.get(pk=1), 'url': 'main_page'},
        {'name': 'О кинотеатре', 'obj': Publication.objects.filter(publication_type=PublicationType.ABOUT).first(),
         'url': 'about'},
        {'name': 'Кафе - Бар', 'obj': Publication.objects.filter(publication_type=PublicationType.CAFE_BAR).first(),
         'url': 'cafe_bar'},
        {'name': 'Vip - зал', 'obj': Publication.objects.filter(publication_type=PublicationType.VIP_HALL).first(),
         'url': 'vip_hall'},
        {'name': 'Реклама', 'obj': Publication.objects.filter(publication_type=PublicationType.ADVERTISING).first(),
         'url': 'advertising'},
        {'name': 'Детская комната', 'obj': Publication.objects.filter(publication_type=PublicationType.CHILDREN_ROOM).first(),
         'url': 'children_room'},
        {'name': 'Контакты', 'obj': ContactsPage.objects.get(pk=1), 'url': 'news'},
    ]

    context = {
        'publications': publications,
        'menu': menu,
    }
    return render(request, 'adminlte/pages/pages_table.html', context)

def main_page(request):
    lang = request.GET.get('lang', 'ru')
    main_page = MainPage.objects.get(pk=1)
    seo = get_object_or_404(SeoMetadata,pk=main_page.seo_id)

    if request.method == 'POST':
        main_form = MainPageForm(request.POST, instance=main_page, prefix='main')
        seo_form = SeoMetadataForm(request.POST, instance=seo, prefix='seo')

        if main_form.is_valid() and seo_form.is_valid():
            seo_instance = seo_form.save()
            main_page_instance = main_form.save()
            main_page_instance.seo = seo_instance
            main_page_instance.save()

        return redirect('pages')
    else:
        main_form = MainPageForm(instance=main_page, prefix='main')
        seo_form = SeoMetadataForm(instance=seo, prefix='seo')

    context = {
        'lang': lang,
        'form': main_form,
        'seo_form': seo_form,
        'menu': menu,
    }
    return render(request,'adminlte/pages/edit/main_page.html',context)


def advertising(request):
    return edit_publication(
        request=request,
        publication_type=PublicationType.ADVERTISING,
        pk=Publication.objects.filter(publication_type=PublicationType.ADVERTISING).first().pk,
        template_name='adminlte/pages/edit/base_pages_edit.html',
        redirect_url='pages'
    )

def children_room(request):
    return edit_publication(
        request=request,
        publication_type=PublicationType.CHILDREN_ROOM,
        pk=Publication.objects.filter(publication_type=PublicationType.CHILDREN_ROOM).first().pk,
        template_name='adminlte/pages/edit/base_pages_edit.html',
        redirect_url='pages'
    )

def about(request):
    return edit_publication(
        request=request,
        pk=Publication.objects.filter(publication_type=PublicationType.ABOUT).first().pk,
        publication_type=PublicationType.ABOUT,
        template_name='adminlte/pages/edit/base_pages_edit.html',
        redirect_url='pages'
    )

def cafe_bar(request):
    return edit_publication(
        request=request,
        pk=Publication.objects.filter(publication_type=PublicationType.CAFE_BAR).first().pk,
        publication_type=PublicationType.CAFE_BAR,
        template_name='adminlte/pages/edit/base_pages_edit.html',
        redirect_url='pages'
    )

def vip_hall(request):
    return edit_publication(
        request=request,
        pk=Publication.objects.filter(publication_type=PublicationType.VIP_HALL).first().pk,
        publication_type=PublicationType.VIP_HALL,
        template_name='adminlte/pages/edit/base_pages_edit.html',
        redirect_url='pages'
    )




def users(request):
    return render(request, 'adminlte/pages/users_table.html', context={'menu': menu})


def mailing(request):
    return render(request, 'adminlte/pages/mailing.html', context={'menu': menu})


def add_publication(request, publication_type, template_name, redirect_url):
    lang = request.GET.get('lang', 'ru')

    if request.method == "POST":
        main_form = PublicationForm(request.POST, request.FILES, prefix="main")
        seo_form = SeoMetadataForm(request.POST, prefix="seo")
        formset = PublicationGalleryFormSet(request.POST, request.FILES, prefix="basegallery_set")

        if main_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                publication_instance = main_form.save(commit=False)
                publication_instance.publication_type = publication_type
                publication_instance.seo = seo_instance
                publication_instance.save()

                formset.instance = publication_instance
                formset.save()
            return redirect(redirect_url)
    else:
        main_form = PublicationForm(prefix="main")
        seo_form = SeoMetadataForm(prefix="seo")
        formset = PublicationGalleryFormSet(prefix="basegallery_set")

    return render(request, template_name, {
        "form": main_form,
        "seo_form": seo_form,
        "lang": lang,
        "formset": formset,
        "publication_type_label": publication_type.label,
        "menu": menu,
    })


def edit_publication(request, pk, publication_type, template_name, redirect_url):
    lang = request.GET.get('lang', 'ru')
    publication = get_object_or_404(Publication, pk=pk)
    seo = get_object_or_404(SeoMetadata, pk=publication.seo_id)

    if request.method == "POST":
        main_form = PublicationForm(request.POST, request.FILES, instance=publication, prefix="main")
        seo_form = SeoMetadataForm(request.POST, instance=seo, prefix="seo")
        formset = PublicationGalleryFormSet(request.POST, request.FILES, instance=publication, prefix="basegallery_set")

        if main_form.is_valid() and seo_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                publication_instance = main_form.save(commit=False)
                publication_instance.seo = seo_instance
                publication_instance.save()

                formset.instance = publication_instance
                formset.save()

            return redirect(redirect_url)
    else:
        main_form = PublicationForm(instance=publication, prefix='main')
        seo_form = SeoMetadataForm(instance=seo, prefix='seo')
        formset = PublicationGalleryFormSet(instance=publication, prefix='basegallery_set')

    return render(request, template_name, {
        'form': main_form,
        'seo_form': seo_form,
        'menu': menu,
        'lang': lang,
        'gallery_images': publication.gallery.all(),
        'publication_type_label': publication_type.label,
        'formset': formset,
    })


def delete_publication(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    publication = get_object_or_404(Publication, pk=pk)
    seo = publication.seo
    images = list(publication.gallery.all())

    try:
        publication.delete()
        if seo:
            seo.delete()
        for img in images:
            img.delete()

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
