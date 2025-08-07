import json

from faker import Faker
import hashlib

fake = Faker()

count = 100

users = []


def hash_string(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


i = 3
for i in range(3, count + 1):
    raw_card_number = ''.join(fake.random_choices(elements='0123456789', length=13))
    raw_password = fake.password(length=10)

    users.append({
        "model": "user.user",
        "id": i,
        "fields": {
            "first_name": fake.first_name()[:20],
            "last_name": fake.last_name()[:20],
            "username": fake.user_name()[:20],
            "email": fake.email()[:20],
            "phone": fake.phone_number()[:20],
            "address": fake.address()[:20],
            "card_number": hash_string(raw_card_number)[:20],
            "language": "uk",
            "gender": "m",
            "birthday": fake.date(),
            "created_at": fake.date(),
            "password": hash_string(raw_password)[:20],
            "city": 1,
        }
    })

with open('../store/users.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, ensure_ascii=False, indent=4)
