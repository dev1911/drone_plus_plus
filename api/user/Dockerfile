FROM python:3.7

RUN mkdir /code
WORKDIR /code

RUN pip install django
RUN pip install django_rest_framework
RUN apt-get update
RUN pip install psycopg2
ADD ./ /code/

CMD ["python3","user/manage.py","runserver","0.0.0.0:8000"]
