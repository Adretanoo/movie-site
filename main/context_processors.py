from adminlte.models import Publication, PublicationType


def menu_header_processor(request):
    return {
        'menu_header': {
            'about': Publication.objects.get(publication_type=PublicationType.ABOUT),
            'cafe_bar': Publication.objects.get(publication_type=PublicationType.CAFE_BAR),
            'vip_hall': Publication.objects.get(publication_type=PublicationType.VIP_HALL),
            'children_room': Publication.objects.get(publication_type=PublicationType.CHILDREN_ROOM),
            'advertisement': Publication.objects.get(publication_type=PublicationType.ADVERTISING),
            'news_pages': Publication.objects.filter(publication_type=PublicationType.NEW_PAGE)
        }
    }
