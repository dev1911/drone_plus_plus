FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD ./ /code/

RUN pip install django
RUN pip install djangorestframework

