from rest_framework import serializers
from drone.models import *


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'

class DroneBatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['id', 'curr_battery']