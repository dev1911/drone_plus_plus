import requests
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from gateway.msgs import *

# Create your views here.

header = {"Api-Token": TOKEN}

# /login
@api_view(['POST',])
@permission_classes((AllowAny,))
def login(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	response = requests.post(user_service + "accounts/login/",data=request.data,headers=header)
	return Response(response.json())

# /register
@api_view(['POST',])
@permission_classes((AllowAny,))
def register(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	response = requests.post(user_service + "accounts/register/", data=request.data,headers=header)
	return Response(response.json())

# /create_order
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_order(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	user_id = requests.get(user_service + "accounts/user_id",data=request.data,headers= header)
	user = user_id.json()['user_id']
	request.data.user_id = user
	order = requests.post(order_service + "api/order/",data={"user_id":user,'latitude':request.data['latitude'],'longitude':request.data['longitude'],'address':request.data['address'] ,'status':request.data['status']},headers=header)
	print(request.data.user_id)
	return Response(order.json())

@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_order(request,order_id):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	print(order_id)
	user_id = requests.get(user_service + "accounts/user_id",data=request.data,headers= header)
	user = user_id.json()['user_id']
	order = requests.put(order_service + "api/order/"+order_id+"/",data={"user_id":user,'latitude':request.data['latitude'],'longitude':request.data['longitude'],'address':request.data['address'] ,'status':request.data['status']},headers=header)
	# print(request.data.user_id)
	return Response(order.json())

@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_order(request,order_id):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	print(order_id)
	user_id = requests.get(user_service + "accounts/user_id",data=request.data,headers= header)
	user = user_id.json()['user_id']
	order = requests.delete(order_service + "api/order/"+order_id+"/")
	# print(request.data.user_id)
	return Response(order)

@api_view(['GET'])
@permission_classes((AllowAny,))
def all_order(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	user_id = requests.get(user_service + "accounts/user_id",data=request.data,headers= header)
	user = user_id.json()['user_id']
	order = requests.get(order_service + "api/order/")
	# print(request.data.user_id)
	return Response(order.json())

@api_view(['POST'])
@permission_classes((AllowAny,))
def create_drone(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	drone = requests.post(logistic_service + "drone/create/",data=request.data,headers=header)
	return Response(drone.json())

@api_view(['GET'])
@permission_classes((AllowAny,))
def list_drone(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	drone = requests.get(logistic_service + "drone/list/",headers=header)
	# print(request.data.user_id)
	return Response(drone.json())

@api_view(['GET'])
@permission_classes((AllowAny,))
def info_drone(request): #not working
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	# drone_id = request.query_params['drone_id']
	# print(drone_id)
	drone = requests.get(logistic_service + "drone/info/",headers=header)
	# print(request.data.user_id)
	return Response(drone.json())

# def current_battery_drone():to be completed

@api_view(['PATCH'])
@permission_classes((AllowAny,))
def change_status(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	drone = requests.patch(logistic_service + "drone/change-status/",data=request.data,headers=header)
	# print(request.data.user_id)
	return Response(drone.json())

@api_view(['PATCH'])
@permission_classes((AllowAny,))
def change_location(request):
	header = {'Authorization':request.META.get("HTTP_AUTHORIZATION",""),"Api-Token":TOKEN}
	print(request.data)
	drone = requests.patch(logistic_service + "drone/change-location/",data=request.data,headers=header)
	# print(request.data.user_id)
	return Response(drone.json())

def drone(request, drone_id):
	return render( request, "index.html", {"drone_id": drone_id})
