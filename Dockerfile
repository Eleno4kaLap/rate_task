FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt install -y \
    gcc \
    libpq-dev

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
