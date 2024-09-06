#FROM --platform=linux/amd64 python:3.10
FROM python:3.10

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && apt-get install -y locales locales-all

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN touch /var/log/access.log
RUN touch /var/log/error.log

COPY . /app