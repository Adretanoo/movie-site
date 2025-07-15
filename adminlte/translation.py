from modeltranslation.translator import translator, TranslationOptions
from .models import Publication, SeoMetadata, Movie

class PublicationTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class SeoMetadataTranslationOptions(TranslationOptions):
    fields = ('title', 'keywords', 'description',)

class MovieTranslationOptions(TranslationOptions):
    fields = {'title','description'}

translator.register(Publication, PublicationTranslationOptions)
translator.register(SeoMetadata, SeoMetadataTranslationOptions)
translator.register(Movie, MovieTranslationOptions)

