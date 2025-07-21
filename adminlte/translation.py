from modeltranslation.translator import translator, TranslationOptions
from .models import Publication, SeoMetadata, Movie, CardHall, CardCinema

class PublicationTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class SeoMetadataTranslationOptions(TranslationOptions):
    fields = ('title', 'keywords', 'description',)

class MovieTranslationOptions(TranslationOptions):
    fields = {'title','description'}

class CardCinemaTranslationOptions(TranslationOptions):
    fields = {'name','description','term'}

class CardHallTranslationOptions(TranslationOptions):
    fields = {'name','description'}


translator.register(Publication, PublicationTranslationOptions)
translator.register(SeoMetadata, SeoMetadataTranslationOptions)
translator.register(Movie, MovieTranslationOptions)
translator.register(CardCinema, CardCinemaTranslationOptions)
translator.register(CardHall, CardHallTranslationOptions)
