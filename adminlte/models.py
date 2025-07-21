import datetime
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
    SPEED_5 = 5, '5с'
    SPEED_10 = 10, '10с'
    SPEED_15 = 15, '15с'


class BackgroundType(models.TextChoices):
    BACKGROUND_PHOTO = 'background_photo', 'Фото на фон'
    JUST_PHOTO = 'just_photo', 'Просто фото'


class PublicationType(models.TextChoices):
    NEWS = 'news', 'Новости'
    SHARES = 'shares', 'Акции'
    ABOUT = 'about', 'Про нас'
    CAFE_BAR = 'cafe_bar', 'Кафе/Бар'
    VIP_HALL = 'vip_hall', 'VIP-зал'
    ADVERTISING = 'advertising', 'Реклама'
    CHILDREN_ROOM = 'children_room', 'Дитяча кімната'

# END ENUMS

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
    card_number = models.CharField(max_length=32) # зашифруй неможна такі дані у відкритому тримати
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
    rotation_speed = models.IntegerField(choices=RotationSpeed.choices, default=RotationSpeed.SPEED_5)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'top_banner'


class TopBannerImage(models.Model):
    banner = models.ForeignKey(TopBanner, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    url = models.URLField()
    text = models.CharField(max_length=255)

    class Meta:
        db_table = 'top_banner_images'


class BackgroundBanner(models.Model):
    image = models.ImageField(upload_to='banners/bg/%Y/%m/%d/')
    background_type = models.CharField(choices=BackgroundType.choices, default=BackgroundType.BACKGROUND_PHOTO, max_length=20)

    def __str__(self):
        return self.image.url

    class Meta:
        db_table = "background_banner"


class NewsBanner(models.Model):
    rotation_speed = models.IntegerField(choices=RotationSpeed.choices, default=RotationSpeed.SPEED_5)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'news_banner'


class NewsBannerImage(models.Model):
    banner = models.ForeignKey(NewsBanner, on_delete=models.CASCADE, related_name='banner_images')
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    url = models.URLField()
    text = models.CharField(max_length=255)

    class Meta:
        db_table = 'news_banner_images'
        unique_together = ('banner', 'image')


# END BANNERS

class SeoMetadata(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "seo_metadata"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    description = models.TextField()
    main_image = models.ImageField(upload_to="movies/main/%Y/%m/%d/")
    url = models.URLField()
    is_2d = models.BooleanField(default=False)
    is_3d = models.BooleanField(default=True)
    is_imax = models.BooleanField(default=False)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="movie_seo")
    gallery = models.ManyToManyField(Images, through='MovieGallery', related_name="movie_galleries")

    def __str__(self):
        return self.title



class MovieGallery(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_gallery'

class CardCinema(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    term = models.TextField()
    logo_image = models.ImageField(upload_to="cinemas/logos/%Y/%m/%d/")
    top_banner = models.ImageField(upload_to="cinemas/banners/%Y/%m/%d/")
    gallery = models.ManyToManyField(Images, through='CardCinemaGallery', related_name="cinema_galleries")
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="card_cinema")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "card_cinema"

class CardCinemaGallery(models.Model):
    card_cinema = models.ForeignKey(CardCinema, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    class Meta:
        db_table = "card_cinema_gallery"

class CardHall(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    schema_image = models.ImageField(upload_to="halls/schema/%Y/%m/%d/")
    top_banner = models.ImageField(upload_to="halls/banners/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)
    gallery = models.ManyToManyField(Images, through='CardHallGallery', related_name="hall_galleries")
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="card_hall")
    card_cinema = models.ForeignKey(CardCinema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "card_hall"

class CardHallGallery(models.Model):
    card_hall = models.ForeignKey(CardHall, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)

    class Meta:
        db_table = "card_hall_gallery"







class Publication(models.Model):
    title = models.CharField(max_length=255)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField()
    main_image = models.ImageField(upload_to="publications/%Y/%m/%d/")
    video_url = models.URLField()
    is_enabled = models.BooleanField(default=True)
    gallery = models.ManyToManyField(Images, through='PublicationGallery', related_name="publication_galleries")
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="publication")
    publication_type = models.CharField(choices=PublicationType.choices, max_length=20)

    def __str__(self):
        return f"{self.title} {self.publication_type}"



class PublicationGallery(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    class Meta:
        db_table = "publication_gallery"




class MainPage(models.Model):
    is_enabled = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    phone_1 = models.CharField(max_length=50)
    phone_2 = models.CharField(max_length=50, blank=True, null=True)
    seo_text = models.TextField(blank=True)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="main_page")

    def __str__(self):
        return f"{self.phone_1}"

    class Meta:
        db_table = "main_page"


class ContactsPage(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    is_enabled = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='contacts/%Y/%m/%d/', blank=True)
    seo = models.OneToOneField(SeoMetadata, on_delete=models.CASCADE, related_name="contacts")

    class Meta:
        db_table = "contacts_page"

    def __str__(self):
        return f"{self.name}"
