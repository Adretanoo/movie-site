from django import forms
from django.forms import DateInput

from .models import Publication, SeoMetadata

class SeoMetadataForm(forms.ModelForm):
    class Meta:
        model = SeoMetadata
        fields = ['url', 'title', 'keywords', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False



class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'published_at', 'description', 'main_image', 'video_url', 'is_enabled']
        widgets = {
            'published_at': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'main_image': forms.ClearableFileInput(attrs={'id': 'mainUpload', 'class': 'd-none'}),
        }
