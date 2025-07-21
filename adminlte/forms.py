from django import forms
from django.forms import DateInput, ClearableFileInput, inlineformset_factory

from .models import Publication, SeoMetadata, Images, TopBanner, TopBannerImage, NewsBanner, NewsBannerImage, \
    BackgroundBanner, Movie, MovieGallery, CardCinema, CardCinemaGallery, CardHall, CardHallGallery, PublicationType, \
    PublicationGallery, MainPage


class PublicationForm(forms.ModelForm):
    title_ru = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название'
    }))
    title_uk = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название'
    }))
    description_ru = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    description_uk = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    published_at = forms.CharField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
    }, format='%Y-%m-%d'))

    video_url = forms.URLField(widget=forms.URLInput(attrs={
        'placeholder': 'Ссылка на видео в youtube'
    }))


    main_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'formPreview',
            'style': 'display: none;',
            'onchange': 'updateImagePreview(this)'
        })
    )
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

class PublicationGalleryForm(forms.ModelForm):
    image_file_upload = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'gallery-file-input', 'accept': 'image/*', 'style': 'display:none'})
    )

    class Meta:
        model = PublicationGallery
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        delete = cleaned_data.get('DELETE')

        if delete:
            return cleaned_data

        uploaded_file = cleaned_data.get('image_file_upload')
        has_existing_image = hasattr(self.instance, 'image') and self.instance.image_id is not None

        if not uploaded_file and not has_existing_image:
            self.add_error('image_file_upload', 'Завантажте зображення або видаліть елемент.')

        return cleaned_data

    def save(self, commit=True):
        image_file = self.cleaned_data.get('image_file_upload')
        if image_file:
            image_instance = Images.objects.create(image_url=image_file)
            self.instance.image = image_instance
        return super().save(commit=commit)

class SeoMetadataForm(forms.ModelForm):
    title_ru = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title'
    }))
    title_uk = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title'
    }))
    description_ru = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Description'
    }))
    description_uk = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Description'
    }))
    keywords_ru = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'word'
    }))
    keywords_uk = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'word'
    }))
    url = forms.URLField(widget=forms.URLInput(attrs={
        'placeholder': 'URL'
    }))

    class Meta:
        model = SeoMetadata
        fields = [
            'url',
            'title_ru', 'title_uk',
            'description_ru', 'description_uk',
            'keywords_ru', 'keywords_uk',
        ]

class BackgroundBannerForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'id': 'formPreview',
        'onchange': 'updateImagePreview(this)',
        'style': 'display: none;',
    }))

    class Meta:
        model = BackgroundBanner
        fields = ['image', 'background_type']
        widgets = {
            'background_type': forms.RadioSelect(attrs={'class': 'option'}),
        }

class TopBannerForm(forms.ModelForm):
    class Meta:
        model = TopBanner
        fields = ['rotation_speed', 'is_enabled']

class TopBannerImageForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        label='Зображення',
        widget=forms.FileInput(attrs={
            'style': 'display:none;',
            'onchange': 'updateImagePreviewUpper(this, "mainPreview__prefix__")',
        })
    )

    class Meta:
        model = TopBannerImage
        fields = ['url', 'text']  # image керуємо вручну
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL',
                'required': 'true'
            }),
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Текст',
                'required': 'true'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        image_file = cleaned_data.get('image_file')
        if not self.instance.pk or (self.instance.pk and not self.instance.image):
            if not image_file:
                self.add_error('image_file', 'Це поле є обов\'язковим.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_file')

        if image_file:
            img = Images.objects.create(image_url=image_file)
            instance.image = img

        if commit:
            instance.save()
        return instance

class NewsBannerForm(forms.ModelForm):
    class Meta:
        model = NewsBanner  # <<< ВИПРАВЛЕНО: Зв'язано з NewsBanner
        fields = ['rotation_speed', 'is_enabled']
        widgets = {
            'rotation_speed': forms.Select(attrs={'class': 'form-select form-select-sm d-inline-block w-auto'},
                                           choices=[(5, '5с'), (10, '10с'), (15, '15с')]),
            'is_enabled': forms.CheckboxInput(attrs={'class': 'custom-switch-input'})
        }

class NewsBannerImageForm(forms.ModelForm):
    image_file_shares = forms.ImageField(
        label='Зображення',
        required=False,
        widget=forms.FileInput(attrs={
            'style': 'display:none;',
            'onchange': 'updateImagePreviewNews(this, "mainPreviewNews__prefix__")',
        })
    )

    class Meta:
        model = NewsBannerImage
        fields = ['url', 'text']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL',
                'required': 'true'
            }),
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Текст',
                'required': 'true'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        image_file_shares = cleaned_data.get('image_file_shares')

        if not self.instance.pk or (self.instance.pk and not self.instance.image):
            if not image_file_shares:
                self.add_error('image_file_shares', 'Це поле є обов\'язковим.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file_shares = self.cleaned_data.get('image_file_shares')

        if image_file_shares:
            try:
                if instance.image:
                    instance.image.delete()
            except NewsBannerImage.image.RelatedObjectDoesNotExist:
                print(
                    f"Попередження: Об'єкт NewsBannerImage (ID: {instance.pk}) має неіснуюче пов'язане зображення. Пропускаємо видалення старого зображення.")
            except Exception as e:
                print(f"Помилка при видаленні старого зображення для NewsBannerImage (ID: {instance.pk}): {e}")

            img = Images.objects.create(image_url=image_file_shares)
            instance.image = img

        elif 'image_file_shares' in self.cleaned_data and self.cleaned_data['image_file_shares'] is False:
            try:
                if instance.image:
                    instance.image.delete()
            except NewsBannerImage.image.RelatedObjectDoesNotExist:
                print(
                    f"Попередження: Об'єкт NewsBannerImage (ID: {instance.pk}) має неіснуюче пов'язане зображення для очищення. Пропущено.")
            except Exception as e:
                print(f"Помилка при очищенні зображення для NewsBannerImage (ID: {instance.pk}): {e}")

        if commit:
            instance.save()
        return instance

class MovieForm(forms.ModelForm):
    title_ru = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название фильма'
    }))
    title_uk = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название фильма'
    }))
    description_ru = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    description_uk = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    published_at = forms.CharField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
    }, format='%Y-%m-%d'))

    url = forms.URLField(widget=forms.URLInput(attrs={
        'placeholder': 'Ссылка на видео'
    }))

    main_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'formPreview',
            'style': 'display: none;',
            'onchange': 'updateImagePreview(this)'
        })
    )

    class Meta:
        model = Movie
        fields = [
            'published_at', 'main_image', 'url',
            'is_2d', 'is_3d', 'is_imax',
            'title_ru', 'title_uk',
            'description_ru', 'description_uk',
        ]

class MovieGalleryForm(forms.ModelForm):
    image_file_upload = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'gallery-file-input', 'accept': 'image/*', 'style': 'display:none'})
    )

    class Meta:
        model = MovieGallery
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        delete = cleaned_data.get('DELETE')

        if delete:
            return cleaned_data

        uploaded_file = cleaned_data.get('image_file_upload')
        has_existing_image = hasattr(self.instance, 'image') and self.instance.image_id is not None

        if not uploaded_file and not has_existing_image:
            self.add_error('image_file_upload', 'Завантажте зображення або видаліть елемент.')

        return cleaned_data

    def save(self, commit=True):
        image_file = self.cleaned_data.get('image_file_upload')
        if image_file:
            image_instance = Images.objects.create(image_url=image_file)
            self.instance.image = image_instance
        return super().save(commit=commit)

class CardCinemaForm(forms.ModelForm):
    name_ru = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название кинотеатра'
    }))
    name_uk = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Название кинотеатра'
    }))
    description_ru = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    description_uk = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    term_ru = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    term_uk = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    logo_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'logoPreviewInput',
            'style': 'display: none;',
            'onchange': 'updateImagePreview(this, "logo")'
        })
    )

    top_banner = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'bannerPreviewInput',
            'style': 'display: none;',
            'onchange': 'updateImagePreview(this, "banner")'
        })
    )

    class Meta:
        model = CardCinema
        fields = ['name_ru', 'name_uk', 'description_ru', 'description_uk', 'term_ru', 'term_uk','top_banner','logo_image']

class CardCinemaGalleryForm(forms.ModelForm):
    image_file_upload = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'gallery-file-input', 'accept': 'image/*', 'style': 'display:none'})
    )

    class Meta:
        model = CardCinemaGallery
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        delete = cleaned_data.get('DELETE')

        if delete:
            return cleaned_data

        uploaded_file = cleaned_data.get('image_file_upload')
        has_existing_image = hasattr(self.instance, 'image') and self.instance.image_id is not None

        if not uploaded_file and not has_existing_image:
            self.add_error('image_file_upload', 'Завантажте зображення або видаліть елемент.')

        return cleaned_data

    def save(self, commit=True):
        image_file = self.cleaned_data.get('image_file_upload')
        if image_file:
            image_instance = Images.objects.create(image_url=image_file)
            self.instance.image = image_instance
        return super().save(commit=commit)

class CardHallForm(forms.ModelForm):
    name_ru = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '8 зал'
    }))
    name_uk = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '8 зал'
    }))
    description_ru = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    description_uk = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))

    schema_image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'logoPreviewInput',
            'style': 'display: none;',
            'onchange': 'updateImagePreview(this, "logo")'
        })
    )

    top_banner = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id': 'bannerPreviewInput',
            'style': 'display: none;',
            'onchange': 'updateImagePreview(this, "banner")'
        })
    )
    class Meta:
        model = CardHall
        fields = ['name_ru', 'name_uk', 'description_ru', 'description_uk','schema_image','top_banner']

class CardHallGalleryForm(forms.ModelForm):
    image_file_upload = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'gallery-file-input', 'accept': 'image/*', 'style': 'display:none'})
    )

    class Meta:
        model = CardHallGallery
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        delete = cleaned_data.get('DELETE')

        if delete:
            return cleaned_data

        uploaded_file = cleaned_data.get('image_file_upload')
        has_existing_image = hasattr(self.instance, 'image') and self.instance.image_id is not None

        if not uploaded_file and not has_existing_image:
            self.add_error('image_file_upload', 'Завантажте зображення або видаліть елемент.')

        return cleaned_data

    def save(self, commit=True):
        image_file = self.cleaned_data.get('image_file_upload')
        if image_file:
            image_instance = Images.objects.create(image_url=image_file)
            self.instance.image = image_instance
        return super().save(commit=commit)

class MainPageForm(forms.ModelForm):
    phone_1 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'tel',
        'placeholder':'777 85 98'
    }))
    phone_2 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'tel',
        'placeholder': '777 85 98'
    }))
    seo_text_ru = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))
    seo_text_uk = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'текст'
    }))

    class Meta:
        model = MainPage
        fields = ['is_enabled','phone_1','phone_2','seo_text_ru','seo_text_uk']








PublicationGalleryFormSet = inlineformset_factory(
    Publication,
    PublicationGallery,
    form=PublicationGalleryForm,
    extra=0,
    can_delete=True
)

CardHallGalleryFormSet = inlineformset_factory(
    CardHall,
    CardHallGallery,
    form=CardHallGalleryForm,
    extra=0,
    can_delete=True
)

CardCinemaGalleryFormSet = inlineformset_factory(
    CardCinema,
    CardCinemaGallery,
    form=CardCinemaGalleryForm,
    extra=0,
    can_delete=True,
)

MovieGalleryFormSet = inlineformset_factory(
    Movie,
    MovieGallery,
    form=MovieGalleryForm,
    extra=0,
    can_delete=True,
)

TopBannerImageFormSet = inlineformset_factory(
    TopBanner,
    TopBannerImage,
    form=TopBannerImageForm,
    extra=0,
    can_delete=True,
)

NewsBannerImageFormSet = inlineformset_factory(
    NewsBanner,
    NewsBannerImage,
    form=NewsBannerImageForm,
    extra=0,
    can_delete=True,
)
