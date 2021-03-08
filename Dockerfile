FROM python:3.9.2-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY . /app

RUN pip install -r requirements.txt
