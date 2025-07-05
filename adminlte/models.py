from random import choices

from django.db import models


# ENUMS
class Gender(models.TextChoices):
    MALE = 'm', 'Male'
    WOMEN = 'w', 'Women'


class Language(models.TextChoices):
    RU = 'ru', 'Russian'
    UK = 'uk', 'Ukrainian'


class RotationSpeed(models.IntegerChoices):
    SPEED_5 = 5
    SPEED_10 = 10
    SPEED_15 = 15


class BackgroundType(models.TextChoices):
    BACKGROUND_PHOTO = 'background_photo'
    JUST_PHOTO = 'just_photo'

class PublicationType(models.TextChoices):
    NEWS = 'news', 'Новини'
    SHARES = 'shares', 'Акції'
    ABOUT = 'about', 'Про нас'
    CAFE_BAR = 'cafe_bar', 'Кафе/Бар'
    VIP_HALL = 'vip_hall', 'VIP-зал'
    ADVERTISING = 'advertising', 'Реклама'
    CHILDREN_ROOM = 'children_room', 'Дитяча кімната'

class ModelType(models.TextChoices):
    MOVIE = 'movie'
    CARD_CINEMA = 'card_cinema'
    CARD_HALL = 'card_hall'
    SEO_METADATA = 'seo_metadata'
    MAIN_PAGE = 'main_page'
    PUBLICATION = 'publication'
    NEWS = 'news', 'Новини'
    SHARES = 'shares', 'Акції'
    ABOUT = 'about', 'Про нас'
    CAFE_BAR = 'cafe_bar', 'Кафе/Бар'
    VIP_HALL = 'vip_hall', 'VIP-зал'
    ADVERTISING = 'advertising', 'Реклама'
    CHILDREN_ROOM = 'children_room', 'Дитяча кімната'


# END ENUMS


class FiledLabelTranslation(models.Model):
    model_name = models.CharField(choices=ModelType.choices) # Publication
    field_name = models.CharField(max_length=100) # title, label, ...
    language_code = models.CharField(choices=Language.choices) # uk, ru
    label = models.TextField(max_length=100) # Заголовок, Телефон

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'filed_label_translation'
        unique_together = ('model_name', 'field_name', 'language_code')

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    password_hash = models.CharField(max_length=255)
    card_number = models.CharField(max_length=32)
    language = models.CharField(choices=Language.choices, max_length=2)
    gender = models.CharField(choices=Gender.choices, max_length=1)
    birthday = models.DateField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username}"


class Images(models.Model):
    image_url = models.ImageField(upload_to='images/%Y/%m/%d/')

    def __str__(self):
        return self.image_url.url


# BANNERS
class TopBanner(models.Model):
    images = models.ManyToManyField(Images)
    url = models.URLField()
    text = models.CharField(max_length=255)
    rotation_speed = models.IntegerField(choices=RotationSpeed.choices, default=RotationSpeed.SPEED_5)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "top_banner"


class BackgroundBanner(models.Model):
    image = models.ImageField(upload_to='banners/bg/%Y/%m/%d/')
    background_type = models.CharField(choices=BackgroundType.choices, default=BackgroundType.BACKGROUND_PHOTO,
                                       max_length=20)

    def __str__(self):
        return self.image.url

    class Meta:
        db_table = "background_banner"


class NewsBanner(models.Model):
    images = models.ManyToManyField(Images)
    url = models.URLField()
    rotation_speed = models.IntegerField(choices=RotationSpeed.choices, default=RotationSpeed.SPEED_5)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Photo url: {self.url}"

    class Meta:
        db_table = "news_banner"


# END BANNERS

class SeoMetadata(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "seo_metadata"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_image = models.ImageField(upload_to="movies/main//%Y/%m/%d/")
    url = models.URLField()
    is_2d = models.BooleanField(default=False)
    is_3d = models.BooleanField(default=True)
    is_imax = models.BooleanField(default=False)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="movie_seo")
    gallery = models.ManyToManyField(Images)

    def __str__(self):
        return self.title


class CardCinema(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    term = models.TextField()
    logo_image = models.ImageField(upload_to="cinemas/logos/%Y/%m/%d/")
    top_banner = models.ImageField(upload_to="cinemas/banners/%Y/%m/%d/")
    gallery = models.ManyToManyField(Images)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="card_cinema")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "card_cinema"


class CardHall(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    schema_image = models.ImageField(upload_to="halls/schema/%Y/%m/%d/", blank=True, null=True)
    top_banner = models.ImageField(upload_to="halls/banners/%Y/%m/%d/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gallery = models.ManyToManyField(Images)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="card_hall")
    card_cinema = models.ForeignKey(CardCinema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "card_hall"


class Publication(models.Model):
    title = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    description = models.TextField()
    main_image = models.ImageField(upload_to="publications/%Y/%m/%d/")
    video_url = models.URLField(blank=True)
    is_enabled = models.BooleanField(default=True)
    gallery = models.ManyToManyField(Images,blank=True)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="publication")
    publication_type = models.CharField(choices=PublicationType.choices, max_length=20)

    def __str__(self):
        return f"{self.title} {self.publication_type}"



class MainPage(models.Model):
    is_enabled = models.BooleanField(default=True)
    phone_1 = models.CharField(max_length=50)
    phone_2 = models.CharField(max_length=50, blank=True, null=True)
    seo_text = models.TextField(blank=True)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="main_page")

    def __str__(self):
        return self.phone_1

    class Meta:
        db_table = "main_page"


class ContactsPage(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True,null=True)
    coordinates = models.CharField(max_length=255,blank=True,null=True)
    is_enabled = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='contacts/%Y/%m/%d/', blank=True)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="contacts")

    class Meta:
        db_table = "contacts_page"







