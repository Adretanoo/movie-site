from django.db import models

from adminlte.models import City, Gender, Language
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20)
    address = models.TextField()
    password_hash = models.CharField(max_length=255)
    card_number = models.CharField(max_length=32)  # зашифруй неможна такі дані у відкритому тримати
    language = models.CharField(choices=Language.choices, max_length=2)
    gender = models.CharField(choices=Gender.choices, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField()

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} "

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username}"
