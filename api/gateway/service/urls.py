from django.urls import path
from django.conf.urls import url
from service.views import *
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('drone/<str:drone_id>', drone, name='drone'),
    path('create_order/',create_order,name='create_order'),
    path('update_order/',update_order,name="update_order"),
    path('delete_order/',delete_order,name="delete_order"),
    path('all_order/',all_order,name="all_order"),
    path('create_drone/',create_drone,name="create_drone"),
    path('list_drone/',list_drone,name="list_drone"),
    path('info_drone/',info_drone,name="info_drone"),
    path('change_status/',change_status,name='change_status'),
    path('change_location/',change_location,name='change_location'),
    path('current_battery/',current_battery,name='current_battery')
]
