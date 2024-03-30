FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y python-dev python-pip python3-dev && apt-get install -y python3-mysqldb curl zip systemd php

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# COPY .env .env

COPY . .


ENV FLASK_APP=./app.py

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=5006"]
EXPOSE 5006
