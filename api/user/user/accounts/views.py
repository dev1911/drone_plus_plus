from django.contrib.auth import login,logout
from rest_framework import status 
from .models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from accounts.serializers import RegistrationSerializer,UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
import json
from django.core import serializers
# Create your views here.

TOKEN = "this_is_token"

def authenticate_api_token(request):
	# checking that this request is from API service
	try:
		token = request.META.get('HTTP_API_TOKEN',"")
		# print(token,TOKEN)
	except:
		return False
	if(token == TOKEN):
		# print("AYA")
		# print(token)
		return True
	else:
		return False

# /accounts/register/
@api_view(['POST',])
def registration_view(request):
	# print("viewww")
	if ((request.method == 'POST') and (authenticate_api_token(request))):
		# print("idhar ayaa")
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			print('working')
			data['response'] = "Successfully registered new user"
			data['username'] = account.username
			data['user_type'] = account.user_type
			token = Token.objects.get(user=account).key
			data['token'] = token
			return Response({'user_info':data},content_type='application/json',status=201)
		else:
			data = serializer.errors
			print(data)
			return Response({'error':data},content_type='application/json',status=400)
	else:
		return Response({'failure':'api authorization token not provided'},content_type='application/json',status=400)
		
# /accounts/logout/
@api_view(['POST',])
# @permission_classes([IsAuthenticated,]) # check hereeee
@authentication_classes([TokenAuthentication])
def logout_view(request):
	try:
		if (authenticate_api_token(request)):
			token = request.META.get("HTTP_AUTHORIZATION","").split()[1]
			logout(request)
			print(request.META.get("HTTP_AUTHORIZATION", ""))
			return Response({'success':"Successfully logged out"},status=200)
	except:
		return Response({'failure':'authentication token not available'},content_type='application/json',status=401)

# /accounts/user_id/
@api_view(['GET',])
def user_id(request):
	if (authenticate_api_token(request)):
		try:
			token = request.META.get("HTTP_AUTHORIZATION","").split()[1]
			print(token)
		except:
			return Response({'failure':'Authorization Token not available'},content_type='application/json',status=400)
		try:
			username = Token.objects.get(key=token)
			print(username.user)
			user_id = User.objects.get(username = username.user)
			print(user_id.pk)
			return Response({'success':'successful','user_id':user_id.pk},content_type='application/json',status=200)
		except:
			return Response({'failure':'User Not Found'},content_type='application/json',status=400)
	else:
		return Response({'failure':'api authorization token not provided'},content_type='application/json',status=400)

# /accounts/disable_user
@api_view(['POST'],)
def disable_user(request):
	# make the is_active false 
	try:
		if request.META.get("HTTP_AUTHORIZATION",""): 
			token = request.META.get("HTTP_AUTHORIZATION","").split()[1]
			username = Token.objects.get(key=token)
	except:
		return Response({'failure':'Authorization Token not available'},content_type='application/json',status=400)
	try:
		current_user = User.objects.get(username=username.user)
		current_user.is_active = False
		current_user.save()
		return Response({"success":"User disabled Successfully"},content_type='application/json',status=200)

	except:
		return Response({'failure':'User Not available'},content_type='application/json',status=400)

# /accounts/user_details
@api_view(['GET'],)
def user_details(request):
	if (authenticate_api_token(request)):
		try:
			token = request.META.get("HTTP_AUTHORIZATION","").split()[1]
			print(token)
		except:
			return Response({'failure':'Authorization Token not available'},content_type='application/json',status=400)
		try:
			username = Token.objects.get(key=token)
			print(username.user)
			# user_type = User.objects.get()
			user_id = User.objects.get(username = username.user)
			print(user_id.pk)
			user_details = User.objects.get(pk = user_id.pk)
			return Response({'success':'successful','username':user_details.username,'user_type':user_details.user_type},content_type='application/json',status=200)
		except:
			return Response({'failure':'User Not available'},content_type='application/json',status=401)
	else:
		return Response({'failure':'api authorization token not provided'},content_type='application/json',status=400)

@api_view(['GET'],)
def all_users(request):
	if (authenticate_api_token(request)):
		try:
			token = request.META.get("HTTP_AUTHORIZATION","").split()[1]
			print(token)
			username = Token.objects.get(key=token)
		except:
			return Response({'failure':'Authorization Token not available'},content_type='application/json',status=400)
		try:
			if(username):
				user = User.objects.all()
				qs = UserSerializer(user,many=True)
				return Response({'success':'successful','all_users':qs.data},content_type='application/json',status=200)
		except:
			return Response({'failure':'User not available'},content_type='application/json',status=401)
	else:
		return Response({'failure':'Api authorization token not provided'},content_type='application/json',status=400)

class Login_view(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,context={'request': request})
		if ((serializer.is_valid()) and (authenticate_api_token(request))):
			user = serializer.validated_data['user']
			token, created = Token.objects.get_or_create(user=user)
			print("Token",request.META.get("HTTP_AUTHORIZATION",""))
			return Response({'token': token.key,'user_id': user.pk,},content_type='application/json',status=200)
		else:
			return Response({'failure':'Credentials not valid'},content_type='application/json',status=400)

