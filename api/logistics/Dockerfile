FROM python:3.7

RUN mkdir /code
WORKDIR /code

RUN pip install django
RUN pip install django_rest_framework
RUN pip install channels
RUN pip install django-cors-headers
RUN pip install requests
RUN pip install psycopg2
RUN pip install websocket_client
ADD ./ /code/

CMD ["python3" , "logistics/manage.py" , "runserver" , "0.0.0.0:8000"]