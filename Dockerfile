# syntax=docker/dockerfile:1

FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY requirements.txt /server

RUN pip install -r requirements.txt

COPY . /server

CMD python manage.py makemigrations && python manage.py migrate
