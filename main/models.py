from django.db import models

from adminlte.models import Movie, CardHall
from user.models import User


class StatusPayment(models.TextChoices):
    BOUGHT = 'bought','Куплено'
    BLOCKED = 'blocked','Заброньовано'


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    card_hall = models.ForeignKey(CardHall, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.movie} - {self.card_hall}'


class Seat(models.Model):
    hall = models.ForeignKey(CardHall, on_delete=models.CASCADE)
    row = models.SmallIntegerField()
    column = models.SmallIntegerField()

    def __str__(self):
        return f'{self.hall} - {self.row} - {self.column}'


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=StatusPayment.choices, max_length=10)

    def __str__(self):
        return f'{self.user} - {self.session} - {self.created_at}'