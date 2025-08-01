from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from adminlte.models import City, Gender, Language
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    card_number = models.CharField(max_length=128)
    language = models.CharField(choices=Language.choices, max_length=2)
    gender = models.CharField(choices=Gender.choices, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField()

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def set_card_number(self, raw_card_number):
        self.card_number = make_password(raw_card_number)

    def check_card_number(self, raw_card_number):
        return check_password(raw_card_number, self.card_number)


    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} "

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username}"
