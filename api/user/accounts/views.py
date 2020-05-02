from django.contrib.auth import login,logout
from rest_framework import status 
from .models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from accounts.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
# Create your views here.

# /accounts/register/
@api_view(['POST',])
def registration_view(request):
	print("viewww")
	if (request.method == 'POST') and (request.META.get("HTTP_API_TOKEN","")):
		print("idhar ayaa")
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
			return Response({'user_info':data},content_type='application/json',status=200)
		else:
			data = serializer.errors
			print(data)
			return Response({'error':data},content_type='application/json',status=500)
	else:
		return Response({'failure':'api authorization token not provided'},content_type='application/json',status=400)
		
# /accounts/logout/
@api_view(['POST',])
# @permission_classes([IsAuthenticated,]) # check hereeee
@authentication_classes([TokenAuthentication])
def logout_view(request):
	if request.META.get("HTTP_AUTHORIZATION",""):
		logout(request)
		print(request.META.get("HTTP_AUTHORIZATION", ""))
		return Response({'success':"Successfully logged out"},status=200)
	else:
		return Response({'header':'authentication header not found'},content_type='application/json',status=401)

# /accounts/user_id/
@api_view(['GET',])
def user_id(request):
	print("TOK",request.META.get("HTTP_API_TOKEN",""))
	print(request.META.get("HTTP_AUTHORIZATION",""))
	print(request.headers)
	if request.META.get("HTTP_API_TOKEN",""):
		token = request.META.get("HTTP_AUTHORIZATION","").split()[1]
		print(token)
		username = Token.objects.get(key=token)
		print(username.user)
		user_id = User.objects.get(username = username.user)
		print(user_id.pk)
		return Response({'success':'successful','user_id':user_id.pk},content_type='application/json',status=200)
	else:
		return Response({'failure':'api authorization token not provided'},content_type='application/json',status=400)

# /accounts/disable_user
@api_view(['POST'],)
def disable_user(request):
	# make the is_active false 
	if request.META.get("HTTP_AUTHORIZATION",""): 
		token = request.META.get("HTTP_AUTHORIZATION","").split()[1]
		username = Token.objects.get(key=token)
		current_user = User.objects.get(username=username.user)
		current_user.is_active = False
		current_user.save()
		return Response({"success":"User disabled Successfully"},content_type='application/json',status=200)
	else:
		return Response({'failure':'user authentication details not provided'},content_type='application/json',status=400)


class Login_view(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,context={'request': request})
		if (  serializer.is_valid()) and (request.META.get("HTTP_API_TOKEN","")):
			user = serializer.validated_data['user']
			token, created = Token.objects.get_or_create(user=user)
			print("TOken",request.META.get("HTTP_AUTHORIZATION",""))
			return Response({'token': token.key,'user_id': user.pk,},content_type='application/json',status=200)
		else:
			return Response({'credentials':'Credentials not provided'},content_type='application/json',status=400)