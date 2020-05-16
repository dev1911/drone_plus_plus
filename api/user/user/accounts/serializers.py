from rest_framework import serializers
from .models import User
class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

	class Meta:
		model= User
		fields=['username','password','password2']
		extra_kwargs={
					'password':{'write_only':True}
		}

	def save(self):
		account = User(username=self.validated_data['username'])
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		# user_type = self.user_type
		if password!=password2:
			raise serializers.ValidationError({'password':'Passwords must match'})

		account.set_password(password)
		account.save()
		return account


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['username','user_type']


