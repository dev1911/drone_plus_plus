from django.urls import path
from drone.views import *

urlpatterns = [
    path('create/', create_drone, name='create_drone'),
    path('list/', list_drones, name='list_drones'),
    path('info/<str:drone_id>/', info_drone, name='info_drone'),
    path('current-battery/<str:drone_id>/', current_battery_drone, name='current_battery_drone'),
    path('change-status/', change_status, name="change_status"),
    path('change-location/', change_location, name="change_location"),
    path('schedule/', schedule, name="schedule"),
    path('path/', path_, name='path')
]
