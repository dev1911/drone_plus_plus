import requests
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from warehouse.serializers import *
from warehouse.models import *
# Create your views here.

@api_view(['GET'])
@permission_classes((AllowAny,))
def warehouses(request):
	a = WarehouseSerializer(Warehouse.objects.all(), many=True)
	return Response(a.data, status=status.HTTP_200_OK)