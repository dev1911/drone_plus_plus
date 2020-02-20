from django.urls import path
from service.views import *
urlpatterns = [
    path('/login', login, 'login'),
]

user_service = "127.0.0.1:8001/"
logistic_service = "127.0.0.1:8002/"
order_service = "127.0.0.1:8003/"
