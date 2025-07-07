from adminlte.models import FiledLabelTranslation

def get_translation(model_name: str, language_code: str) -> dict:
    translations = (
        FiledLabelTranslation.objects.filter(model_name=model_name,language_code=language_code).values_list('field_name','label')
    )
    return dict(translations)