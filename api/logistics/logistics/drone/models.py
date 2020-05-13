from django.db import models
from warehouse.models import Warehouse
# Create your models here.

class Drone(models.Model):
    owner = models.CharField(null=False, blank=True, max_length=256)
    battery = models.FloatField(null=False, blank=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True)
    curr_battery = models.FloatField(null=False, blank=False, default=0)
    status = models.CharField(max_length=10, choices=(("Idle", "Idle"),
                                       ("Charging", "Charging"),
                                       ("Delivering", "Delivering"),
                                       ("Returning", "Returning"),
                                       ("Offline", "Offline")))
    curr_latitude = models.FloatField(null=True, blank=True)
    curr_longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.owner+" Drone "+str(self.id)