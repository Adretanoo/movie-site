FROM python:3.11-slim

WORKDIR /app
COPY . /app/


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000
COPY /config/app/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh



ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["uvicorn", "cinemasite.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]