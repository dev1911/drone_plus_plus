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

header = {"HTTP_API_TOKEN": TOKEN}


# /login
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    response = requests.post(user_service + "accounts/login/", data=request.data, headers=header)
    return response


# /register
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    response = requests.post(user_service + "/register", data=request.urls, headers=header)
    return response


def drone(request, drone_id):
    return render( request, "index.html", {"drone_id": drone_id})
