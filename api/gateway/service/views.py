import requests
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from service.urls import user_service, logistic_service, order_service
# Create your views here.


# /login
@api_view(['POST'])
@permission_classes((AllowAny,))
def login():
    try:
        data = {'username':requests.data['username'], 'password':requests.data['password']}
    except:
        return Response()
    response = requests.post(user_service, data=data)
