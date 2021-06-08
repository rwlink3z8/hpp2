# syntax=docker/dockerfile:1
FROM python:3.8-slim as production 
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update -y && \
apt-get install -y python-pip python-dev
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements/prod.txt ./requirements/prod.txt
COPY app/data  ./app/data
RUN pip install -r ./requirements/prod.txt 
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
