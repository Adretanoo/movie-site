from django import forms
from django.forms import DateInput, ClearableFileInput
from .models import Publication, SeoMetadata


class PublicationForm(forms.ModelForm):
    # без gallery у fields
    class Meta:
        model = Publication
        fields = [
            'title_ru', 'title_uk',
            'description_ru', 'description_uk',
            'published_at',
            'main_image',
            'video_url',
            'is_enabled',
        ]
        widgets = {
            'published_at': DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'main_image': ClearableFileInput(attrs={'id': 'mainUpload', 'class': 'd-none', 'accept': 'image/*'}),
        }


class SeoMetadataForm(forms.ModelForm):
    class Meta:
        model = SeoMetadata
        fields = [
            'url',
            'title_ru', 'title_uk',
            'keywords_ru', 'keywords_uk',
            'description_ru', 'description_uk',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs.update({'class': 'form-control'})
