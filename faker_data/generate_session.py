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
from adminlte.models import Movie, CardHall

faker = Faker()

today_date = datetime.today() - timedelta(days=1)
end_date = today_date + timedelta(days=30)


item = 0


with open("../store/movies.json") as f:
    movies = json.load(f)
halls = CardHall.objects.all()

session = []

for h in halls:
    for m in movies:
        session.append({
            "model": "main.Session",
            "pk": item,
            "fields": {
                "movie": m["pk"],
                "card_hall": h["pk"],
                "start_time": faker.date_time_between(start_date=today_date, end_date=end_date, ).strftime(
                    '%Y-%m-%dT%H:%M:%SZ'),
                "price": int(Decimal(str(round(random.uniform(10, 100))))),
            }
        })
        item += 1



with open('../store/sessions.json', 'w', encoding='utf-8') as f:
    json.dump(session, f, ensure_ascii=False, indent=4)


# hall = CardHall.objects.get(pk=4)
#
# for row in range(1, 11):
#     for col in range(1, 11):
#         Seat.objects.create(hall=hall,row=row,column=col)
