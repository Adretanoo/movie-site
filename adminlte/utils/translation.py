from adminlte.models import FiledValueTranslation

def get_translation(model_name: str, language_code: str) -> dict:
    translations = (
        FiledValueTranslation.objects.filter(model_name=model_name,language_code=language_code).values_list('field_name','value')
    )
    return dict(translations)