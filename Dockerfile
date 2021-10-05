FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
