FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /book_store
COPY . .

RUN pip3 install -r requirements.txt

CMD gunicorn book_store.wsgi:application --bind 0.0.0.0:$PORT

