
from modeltranslation.translator import translator, TranslationOptions
from .models import Publication, SeoMetadata

class PublicationTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class SeoMetadataTranslationOptions(TranslationOptions):
    fields = ('title', 'keywords', 'description',)

translator.register(Publication, PublicationTranslationOptions)
translator.register(SeoMetadata, SeoMetadataTranslationOptions)