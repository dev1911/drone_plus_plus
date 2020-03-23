from django.db import models

# Create your models here.
class Order(models.Model):
	order_id = models.AutoField(primary_key=True)
	user_id = models.CharField(unique=False,max_length=100)
	latitude = models.FloatField(max_length=20)
	longitude = models.FloatField(max_length=20)
	address = models.CharField(unique=False,max_length=500)
	status = models.CharField(max_length=20 , choices= (("Completed" , "Completed"),
														("Pending" , "Pending"),
														("Error" , "Error"),
														("Ongoing" , "Ongoing")) ,
														default="Pending")
	def __str__(self):
		return self.order_id + "\n" + self.user_id + "\n" + self.address