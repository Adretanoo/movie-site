import os
from _pydatetime import timedelta

import requests
import json
from datetime import datetime, timedelta

from dulwich.config import lower_key
from faker import Faker

from cinemasite import settings

faker = Faker('ru_RU')

API_KEY = '9a40da80a34cda55150f8479cef091f3'
LANG_UK = "uk-UA"
LANG_RU = "ru-RU"

today_date = datetime.today()
end_date = today_date + timedelta(days=30)

page_total = 3
item = 0
seo_item = 15
movies = []
seo = []

for page in range(1, page_total + 1):
    url_ru = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language={LANG_RU}&page={page}"
    response_ru = requests.get(url_ru)
    data_ru = response_ru.json()

    for movie in data_ru["results"]:
        title = movie["title"]
        keywords = faker.words()
        description = movie["overview"]

        seo.append({
            "model": "adminlte.seometadata",
            "pk": seo_item,
            "fields": {
                "url": "https://www.youtube.com/embed/j-iheFkstFQ",
                "title": f"Фильм {title}",
                "keywords": keywords,
                "description": description,
            }
        })
        seo_item += 1

seo_item = 15
for page in range(1, page_total + 1):
    url_uk = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language={LANG_UK}&page={page}"
    url_ru = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language={LANG_RU}&page={page}"

    response_uk = requests.get(url_uk)
    response_ru = requests.get(url_ru)

    data_uk = response_uk.json()
    data_ru = response_ru.json()

    for movie_uk, movie_ru in zip(data_uk["results"], data_ru["results"]):
        title_ru = movie_ru["title"]
        title_uk = movie_uk['title']
        description_uk = movie_uk['overview']
        description_ru = movie_ru['overview']

        main_url = "https://image.tmdb.org/t/p/w500" + movie_uk['poster_path']
        image_name = movie_uk['poster_path'].split('/')[-1]

        relative_image_path_to_save = os.path.join('movies/main', today_date.strftime('%Y/%m/%d'))
        image_dir = os.path.join(settings.MEDIA_ROOT, relative_image_path_to_save)
        os.makedirs(image_dir, exist_ok=True)

        image_path = os.path.join(image_dir, image_name)

        try:
            image_response = requests.get(main_url)
            image_response.raise_for_status()

            with open(image_path, 'wb') as f:
                f.write(image_response.content)

            fixture_image_path = os.path.join(relative_image_path_to_save, image_name)

        except requests.exceptions.RequestException as e:
            fixture_image_path = ""

        movies.append({
            "model": "adminlte.movie",
            "pk": item,
            "fields": {
                "title": title_ru,
                "title_ru": title_ru,
                "title_uk": title_uk,
                "published_at": faker.date_between(start_date=today_date, end_date=end_date, ).strftime(
                    '%Y-%m-%dT%H:%M:%SZ'),
                "description": description_ru,
                "description_ru": description_ru,
                "description_uk": description_uk,
                "main_image": fixture_image_path,
                "url": 'https://www.youtube.com/embed/j-iheFkstFQ',
                "is_2d": faker.pybool(),
                "is_3d": faker.pybool(),
                "is_imax": True,
                "seo": seo_item,

            }
        })
        item += 1
        seo_item += 1

with open('../store/seo_movie.json', 'w', encoding='utf-8') as f:
    json.dump(seo, f, ensure_ascii=False, indent=4)

with open('../store/movies.json', 'w', encoding='utf-8') as f:
    json.dump(movies, f, ensure_ascii=False, indent=4)
