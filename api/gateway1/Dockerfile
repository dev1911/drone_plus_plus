FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code

RUN pip install django
RUN pip install django_rest_framework

ADD ./ /code/

CMD ["python3" , "gateway/manage.py" , "runserver" , "0.0.0.0:8000"]