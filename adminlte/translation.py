from modeltranslation.translator import translator, TranslationOptions
from .models import Publication, SeoMetadata, Movie, CardHall, CardCinema, MainPage


class PublicationTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)



class MovieTranslationOptions(TranslationOptions):
    fields = {'title','description'}

class CardCinemaTranslationOptions(TranslationOptions):
    fields = {'name','description','term'}

class CardHallTranslationOptions(TranslationOptions):
    fields = {'name','description'}

class MainPageTranslationOptions(TranslationOptions):
    fields = {'seo_text'}


translator.register(Publication, PublicationTranslationOptions)
translator.register(Movie, MovieTranslationOptions)
translator.register(CardCinema, CardCinemaTranslationOptions)
translator.register(CardHall, CardHallTranslationOptions)
translator.register(MainPage, MainPageTranslationOptions)
