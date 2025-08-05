import json
import os
import random
from decimal import Decimal

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinemasite.settings')
django.setup()

# from main.models import Seat
# from adminlte.models import CardHall
from faker import Faker
from datetime import datetime, timedelta
from decimal import Decimal
import random
from adminlte.models import Movie, CardHall

faker = Faker()

item = 0
movies = Movie.objects.all()
halls = CardHall.objects.all()
session = []

for m in movies:
    movie_publish_date = m.published_at  # припускаємо, що це datetime або date
    session_start = movie_publish_date + timedelta(days=1)
    session_end = session_start + timedelta(days=5)

    for h in halls:
        session_time = faker.date_time_between(start_date=session_start, end_date=session_end)

        session.append({
            "model": "main.Session",
            "pk": item,
            "fields": {
                "movie": m.id,
                "card_hall": h.id,
                "start_time": session_time.isoformat(),  # напр. 2025-08-07T14:00:00
                "price": int(Decimal(str(round(random.uniform(10, 100))))),
            }
        })
        item += 1

with open('../store/sessions.json', 'w', encoding='utf-8') as f:
    json.dump(session, f, ensure_ascii=False, indent=4, default=str)

# hall = CardHall.objects.get(pk=4)
#
# for row in range(1, 11):
#     for col in range(1, 11):
#         Seat.objects.create(hall=hall,row=row,column=col)
