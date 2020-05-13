from django.db import models

# Create your models here.
class Warehouse(models.Model):
    name = models.TextField(null=False, blank=True, unique=True)
    latitude = models.FloatField(null=False, blank=True)
    longitude = models.FloatField(null=False, blank=True)

    def __str__(self):
        return self.name