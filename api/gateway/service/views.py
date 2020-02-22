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
    response = requests.post(user_service + "accounts/register", data=request.data, headers=header)
    return response

# /my-orders
@api_view(['GET'])
@permission_classes((AllowAny,))
def my_orders(request):
    try:
        response = requests.post(user_service+"accounts/user_id", data=request.data, headers=header+{"HTTP_USER_TOKEN": request.META['HTTP_USER_TOKEN']})
    except:
        return Response({"error": token_error}, status=status.HTTP_401_UNAUTHORIZED)
    if response.status_code == status.HTTP_200_OK:
        pass
    
def drone(request, drone_id):
    return render( request, "index.html", {"drone_id": drone_id})
