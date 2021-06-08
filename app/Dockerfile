FROM python:3.8-slim as production 
ENV PYTHONUNBUFFERED=1
WORKDIR /app/
RUN apt-get update -y && \
apt-get install -y python-pip python-dev

COPY requirements/prod.txt ./requirements/prod.txt
RUN pip install -r ./requirements/prod.txt 
COPY . /app
EXPOSE 5000

COPY . .
