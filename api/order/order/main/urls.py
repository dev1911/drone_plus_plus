from django.contrib import admin
from django.urls import path , include
from .views import OrderViewSet
from rest_framework import routers
# from .api import router

# urlpatterns = [
#     path('api/order' , include(router.urls)),
# ]