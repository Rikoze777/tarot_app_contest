FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tarot
COPY . /tarot
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN SECRET_KEY=NOT_IMPORTANT_VALUE python manage.py to_db
EXPOSE 80


CMD ["python", "-m", "gunicorn", "-b", "127.0.0.1:8080", "zodiac.wsgi:application"]