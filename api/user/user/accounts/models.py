from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
USER_TYPE = (('client','client'),
			('logistics_operator','logistics_operator'))
class User(AbstractUser):
	user_type = models.CharField(max_length=20,choices=USER_TYPE,default="client")

	
@receiver(post_save,sender=User)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)


