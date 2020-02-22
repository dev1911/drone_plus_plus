from django.urls import path
from service.views import *
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('drone/<str:drone_id>', drone, name='drone')
]
