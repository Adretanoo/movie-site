from faker import Faker
import random

fake = Faker()


def generate_fake_users(n=10):
    users = []
    for i in range(n):
        users.append({
            'id': i + 1,
            'created': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            'birthday': fake.date_of_birth().strftime('%Y-%m-%d'),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'fio': f"{fake.first_name()} {fake.last_name()}",
            'username': fake.user_name(),
            'city': fake.city()
        })
    return users
