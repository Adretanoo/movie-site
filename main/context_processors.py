from adminlte.models import Publication, PublicationType


def menu_header_processor(request):
    return {
        'menu_header': {
            'about': Publication.objects.filter(publication_type=PublicationType.ABOUT).first(),
            'cafe_bar': Publication.objects.filter(publication_type=PublicationType.CAFE_BAR).first(),
            'vip_hall': Publication.objects.filter(publication_type=PublicationType.VIP_HALL).first(),
            'children_room': Publication.objects.filter(publication_type=PublicationType.CHILDREN_ROOM).first(),
            'advertisement': Publication.objects.filter(publication_type=PublicationType.ADVERTISING).first(),
            'news_pages': Publication.objects.filter(publication_type=PublicationType.NEW_PAGE),
        }
    }
