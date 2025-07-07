from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .utils.translation import get_translation
from adminlte.models import Publication, Images, PublicationType
from .forms import PublicationForm, SeoMetadataForm

menu = [
    {'title': 'Статистика', 'url_name': 'statistics', 'group': ['statistics'], 'icon': 'fa-chart-line'},
    {'title': 'Баннера/Слайдеры', 'url_name': 'banners-sliders', 'group': ['banners-sliders'], 'icon': 'fa-image'},
    {'title': 'Фильмы', 'url_name': 'movies', 'group': ['movies'], 'icon': 'fa-film'},
    {'title': 'Кинотеатры', 'url_name': 'cinemas', 'group': ['cinemas'], 'icon': 'fa-building'},
    {'title': 'Новости', 'url_name': 'news', 'group': ['news', 'add_news', 'edit_news'], 'icon': 'fa-newspaper'},
    {'title': 'Акции', 'url_name': 'shares', 'group': ['shares','add_shares','edit_shares'], 'icon': 'fa-tags'},
    {'title': 'Страницы', 'url_name': 'pages', 'group': ['pages'], 'icon': 'fa-file-alt'},
    {'title': 'Пользователи', 'url_name': 'users', 'group': ['users'], 'icon': 'fa-users'},
    {'title': 'Рассылка', 'url_name': 'mailing', 'group': ['mailing'], 'icon': 'fa-envelope'},
]


def statistics(request):
    return render(request, "adminlte/pages/statistics.html", context={'menu': menu})


def banners_sliders(request):
    return render(request, 'adminlte/pages/banners_sliders_table.html', context={'menu': menu})


def movies(request):
    return render(request, 'adminlte/pages/movies_table.html', context={'menu': menu})


def cinemas(request):
    return render(request, 'adminlte/pages/cinemas_table.html', context={'menu': menu})


def news(request):
    publications = Publication.objects.filter(publication_type=PublicationType.NEWS)
    return render(request, 'adminlte/pages/news_tabel.html', context={'menu': menu, 'publications': publications})


def news_add(request):
    return add_publication(
        request=request,
        publication_type=PublicationType.NEWS,
        template_name='adminlte/pages/add/base_add.html',
        translation_key=PublicationType.NEWS,
        redirect_url='news'
    )


@require_POST
def delete_news(request, pk):
    return delete_publication(
        request=request,
        pk=pk,
        publication_type=PublicationType.NEWS,
        redirect_url='news'
    )


def edit_news(request, pk):
    return edit_publication(
        request=request,
        pk=pk,
        publication_type=PublicationType.NEWS,
        template_name='adminlte/pages/edit/base_edit.html',
        translation_key=PublicationType.NEWS,
        redirect_url='news'
    )


def shares(request):
    publications = Publication.objects.filter(publication_type=PublicationType.SHARES)
    return render(request, 'adminlte/pages/shares_tabel.html', context={'menu': menu, 'publications': publications})

def add_shares(request):
    return add_publication(
        request=request,
        publication_type=PublicationType.SHARES,
        template_name='adminlte/pages/add/base_add.html',
        translation_key=PublicationType.SHARES,
        redirect_url='shares'
    )


@require_POST
def delete_shares(request, pk):
    return delete_publication(
        request=request,
        pk=pk,
        publication_type=PublicationType.SHARES,
        redirect_url='shares'
    )


def edit_shares(request, pk):
    return edit_publication(
        request=request,
        pk=pk,
        publication_type=PublicationType.SHARES,
        template_name='adminlte/pages/edit/base_edit.html',
        translation_key=PublicationType.SHARES,
        redirect_url='shares'
    )


def pages(request):
    return render(request, 'adminlte/pages/pages_table.html', context={'menu': menu})


def users(request):
    return render(request, 'adminlte/pages/users_table.html', context={'menu': menu})


def mailing(request):
    return render(request, 'adminlte/pages/mailing.html', context={'menu': menu})


def add_publication(request, publication_type, template_name, translation_key, redirect_url):
    language = request.GET.get('lang', 'ru')
    t = get_translation(translation_key, language)

    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES, prefix='pub')
        seo_form = SeoMetadataForm(request.POST, prefix='seo')
        if form.is_valid() and seo_form.is_valid():
            with transaction.atomic():
                seo_instance = seo_form.save()
                publication = form.save(commit=False)
                publication.publication_type = publication_type
                publication.seo = seo_instance
                publication.save()
                form.save_m2m()

                for f in request.FILES.getlist('gallery_images'):
                    img = Images.objects.create(image_url=f)
                    publication.gallery.add(img)

            return redirect(redirect_url)
    else:
        form = PublicationForm(prefix='pub')
        seo_form = SeoMetadataForm(prefix='seo')

    return render(request, template_name, {
        'menu': menu,
        'form': form,
        'seo_form': seo_form,
        't': t,
        'lang': language,
    })


def edit_publication(request, pk, publication_type, template_name, translation_key, redirect_url):
    publication = get_object_or_404(Publication, pk=pk)
    seo_instance = publication.seo

    language = request.GET.get('lang', 'ru')
    t = get_translation(translation_key, language)

    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES, instance=publication, prefix='pub')
        seo_form = SeoMetadataForm(request.POST, instance=seo_instance, prefix='seo')

        if form.is_valid() and seo_form.is_valid():
            with transaction.atomic():
                seo = seo_form.save()
                pub = form.save(commit=False)
                pub.seo = seo
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
        'menu': menu,
        'form': form,
        'seo_form': seo_form,
        't': t,
        'lang': language,
        'gallery_images': publication.gallery.all(),
    })


@require_POST
def delete_publication(request, pk, publication_type, redirect_url):
    publication = get_object_or_404(Publication, pk=pk)
    seo = publication.seo
    images = list(publication.gallery.all())

    publication.delete()
    if seo:
        seo.delete()
    for img in images:
        img.delete()

    return redirect(redirect_url)

