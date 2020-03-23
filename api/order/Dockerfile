FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN pip install django
RUN pip install django_rest_framework
ADD ./ /code/
CMD ["python", "order/manage.py" , "makemigrations"]
CMD ["python", "order/manage.py" , "migrate"]
CMD ["python", "order/manage.py", "runserver", "0.0.0.0:8001"]
