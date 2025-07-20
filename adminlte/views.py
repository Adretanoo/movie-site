import datetime

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from adminlte.models import Publication, Images, PublicationType, TopBanner, NewsBanner, BackgroundBanner, \
    TopBannerImage, NewsBannerImage, Movie, MovieGallery, SeoMetadata
from .forms import PublicationForm, SeoMetadataForm, BackgroundBannerForm, TopBannerForm, TopBannerImageForm, \
    TopBannerImageFormSet, NewsBannerForm, NewsBannerImageFormSet, MovieForm, MovieGalleryFormSet
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
                            # Видалити форму навіть якщо вона невалідна, але позначена на видалення
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
                            # Якщо форма невалідна, але позначена на видалення — видаляємо вручну
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
    }
    return render(request, 'adminlte/pages/edit/movies_edit.html', context)


@require_POST
def movies_delete(request):
    movie_id = request.POST.get('movie_id')
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    messages.success(request, f'Фільм "{movie.title}" було успішно видалено.')
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
    return render(request, 'adminlte/pages/cinemas_display.html', context={'menu': menu})


def cinemas(request):
    return render(request, 'adminlte/pages/cinemas_display.html', context={'menu': menu})

def cinemas_add(request):
    lang = request.GET.get('lang', 'ru')

    context = {
        'menu': menu,
        'lang': lang,
    }
    return render(request,'adminlte/pages/add/cinemas_add.html', context)

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
    return render(request, 'adminlte/pages/pages_table.html', context={'menu': menu})


def users(request):
    return render(request, 'adminlte/pages/users_table.html', context={'menu': menu})


def mailing(request):
    return render(request, 'adminlte/pages/mailing.html', context={'menu': menu})


def add_publication(request, publication_type, template_name, redirect_url):
    language = request.GET.get('lang', 'ru')

    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES, prefix="pub")
        seo_form = SeoMetadataForm(request.POST, prefix="seo")

        if form.is_valid() and seo_form.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                publication = form.save(commit=False)
                publication.publication_type = publication_type
                publication.seo = seo_instance
                publication.save()
                form.save_m2m()

                for f in request.FILES.getlist("gallery_images"):
                    img = Images.objects.create(image_url=f)
                    publication.gallery.add(img)

            return redirect(redirect_url)
    else:
        form = PublicationForm(prefix="pub")
        seo_form = SeoMetadataForm(prefix="seo")

    return render(request, template_name, {
        "form": form,
        "seo_form": seo_form,
        "lang": language,
        "publication_type_label": publication_type.label,
        "menu": menu,
    })


def edit_publication(request, pk, publication_type, template_name, redirect_url):
    publication = get_object_or_404(Publication, pk=pk)
    seo_instance = publication.seo

    language = request.GET.get('lang', 'ru')

    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES, instance=publication, prefix='pub')
        seo_form = SeoMetadataForm(request.POST, instance=seo_instance, prefix='seo')

        if form.is_valid() and seo_form.is_valid():
            with transaction.atomic():
                seo = seo_form.save()
                pub = form.save(commit=False)
                pub.seo = seo

                pub.published_at = form.cleaned_data.get('published_at')

                pub.save()
                form.save_m2m()

                images_to_delete = request.POST.get("images_to_delete", "")
                if images_to_delete:
                    ids = [int(i) for i in images_to_delete.split(",") if i.strip().isdigit()]
                    for image in Images.objects.filter(id__in=ids):
                        pub.gallery.remove(image)
                        image.delete()

                for f in request.FILES.getlist('gallery_images'):
                    img = Images.objects.create(image_url=f)
                    pub.gallery.add(img)

            return redirect(redirect_url)

    else:
        form = PublicationForm(instance=publication, prefix='pub')
        seo_form = SeoMetadataForm(instance=seo_instance, prefix='seo')

    return render(request, template_name, {
        'form': form,
        'seo_form': seo_form,
        'menu': menu,
        'lang': language,
        'gallery_images': publication.gallery.all(),
        'publication_type_label': publication_type.label,
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
