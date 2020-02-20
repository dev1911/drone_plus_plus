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

header = {"HTTP_API_TOKEN" : API_TOKEN}

# /login
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    response = requests.post(user_service + "login/", data=request.data, headers=header)
    return Response(response, status=response.status_code)

# /register
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    response = requests.post(user_service+"/register", data=request.urls, headers=header)
    return Response(response, status=response.status_code)