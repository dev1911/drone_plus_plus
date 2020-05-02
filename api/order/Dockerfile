FROM python:3.7

RUN mkdir /code
WORKDIR /code

RUN pip install django
RUN pip install django_rest_framework
RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev
RUN pip install mysqlclient
ADD ./ /code/

CMD ["python3","order/manage.py","runserver","0.0.0.0:8000"]
