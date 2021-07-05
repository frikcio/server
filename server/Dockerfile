# syntax=docker/dockerfile:1

FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /home/server

COPY requirements.txt /home/server

RUN pip install -r requirements.txt

COPY . /home/server
