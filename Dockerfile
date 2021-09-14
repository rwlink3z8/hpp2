# syntax=docker/dockerfile:1
FROM python:3.8

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

WORKDIR ./app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# COPY requirements.txt .

COPY ./requirements.txt /app/requirements.txt
COPY ./data  ./app/data
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app
