from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
import json
from accounts.serializers import *
from accounts.models import *

header = {"HTTP_API_TOKEN":"this_is_token"}
# Create your tests here.

class RegisterNewUser(APITestCase):

	######################
	# Register New User #
	######################

	# success tests
	def test_create_0(self):
		"""
		Registering a New User 
		"""
		# url = reverse('registration_view')
		url = '/accounts/register/'
		data = {"username": "test","password":"password","password2":"password"}
		response = self.client.post(url, data, format='json', **header)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.count(), 1)

	# failed tests
	def test_create_1(self):
		"""
		Registering a New User with passwords not matching
		"""
		url = '/accounts/register/'
		data = {"username": "test","password":"password","password2":"password2"}
		response = self.client.post(url, data, format='json', **header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_2(self):
		"""
		Registering a New User without password confirmation
		"""
		url = '/accounts/register/'
		data = {"username": "test","password":"password"}
		response = self.client.post(url, data, format='json', **header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_3(self):
		"""
		Registering a New User without username
		"""
		url = '/accounts/register/'
		data = {"password":"password","password2":"password"}
		response = self.client.post(url, data, format='json', **header)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_3(self):
		"""
		API Token Not provided
		"""
		url = '/accounts/register/'
		data = {"username":"test","password":"password","password2":"password"}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class LoginUser(APITestCase):

# 	def setUp(self):
# 		self.username = "test1"
# 		self.password = "password"
# 		self.user = User.objects.create_user(self.username,self.password)
# 		self.token,self.created = Token.objects.get_or_create(user=self.user)

# 	def test_login_0(self):
# 		url = '/accounts/login/'
# 		data = {"username":"test1","password":"password"}
# 		response = self.client.post(url, data, format='json',HTTP_API_TOKEN="this_is_token")
# 		self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserId(APITestCase):

	######################
	# GET USER ID #
	######################

	def setUp(self):
		self.username = "test1"
		self.password = "password"
		self.user = User.objects.create_user(self.username,self.password)
		self.token,self.created = Token.objects.get_or_create(user=self.user)
		# print(self.token)

	# success tests
	def test_user_id_0(self):
		'''
		User Token Provided
		'''
		url = '/accounts/user_id/'
		response = self.client.get(url,HTTP_AUTHORIZATION='Token '+ self.token.key,HTTP_API_TOKEN="this_is_token")
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#failure tests
	def test_user_id_1(self):
		'''
		User Token Not Provided
		'''
		url = '/accounts/user_id/'
		response = self.client.get(url,HTTP_API_TOKEN="this_is_token")
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserDetails(APITestCase):

	######################
	# GET USER DETAILS #
	######################

	def setUp(self):
		self.username = "test1"
		self.password = "password"
		self.user = User.objects.create_user(self.username,self.password)
		self.token,self.created = Token.objects.get_or_create(user=self.user)
		# print(self.token)

	# success tests
	def test_user_details_0(self):
		'''
		User Token Provided
		'''
		url = '/accounts/user_details/'
		response = self.client.get(url,HTTP_AUTHORIZATION='Token '+ self.token.key,HTTP_API_TOKEN="this_is_token")
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#failure tests
	def test_user_details_1(self):
		'''
		User Token Not Provided
		'''
		url = '/accounts/user_details/'
		response = self.client.get(url,HTTP_API_TOKEN="this_is_token")
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_user_details_2(self):
		'''
		User Token Provided Is Invalid
		'''
		url = '/accounts/user_details/'
		response = self.client.get(url,HTTP_AUTHORIZATION='Token '+ 'f66fe3fa4f5e382e24c31fcb0c0e0ed750fa5a68',HTTP_API_TOKEN="this_is_token")
		print(response.content)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_user_details_3(self):
		'''
		API Token Not Provided
		'''
		url = '/accounts/user_details/'
		response = self.client.get(url,HTTP_AUTHORIZATION='Token '+ self.token.key)
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AllUser(APITestCase):

	######################
	# GET ALL USERS #
	######################

	def setUp(self):
		self.username = "test1"
		self.password = "password"
		self.user = User.objects.create_user(self.username,self.password)
		self.token,self.created = Token.objects.get_or_create(user=self.user)
		# print(self.token)

	# success tests
	def test_user_0(self):
		'''
		User Token Provided
		'''
		url = '/accounts/all_users/'
		response = self.client.get(url,HTTP_AUTHORIZATION='Token '+ self.token.key,HTTP_API_TOKEN="this_is_token")
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#failure tests
	def test_user_1(self):
		'''
		User Token Not Provided
		'''
		url = '/accounts/all_users/'
		response = self.client.get(url,HTTP_API_TOKEN="this_is_token")
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_user_2(self):
		'''
		User Token Provided Is Invalid
		'''
		url = '/accounts/all_users/'
		response = self.client.get(url,HTTP_AUTHORIZATION='Token '+ 'f66fe3fa4f5e382e24c31fcb0c0e0ed750fa5a68',HTTP_API_TOKEN="this_is_token")
		print(response.content)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_user_3(self):
		'''
		API Token Not Provided
		'''
		url = '/accounts/all_users/'
		response = self.client.get(url,HTTP_AUTHORIZATION='Token '+ self.token.key)
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

   