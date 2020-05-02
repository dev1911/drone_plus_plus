from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drone.models import Drone
from warehouse.models import Warehouse
from logistics.msgs import *
from .serializers import *
# Create your views here.


# reusable functions

def authenticate_api_token(request):
    # checking that this request is from API service
    try:
        # print(request.META)
        token = request.META['HTTP_API_TOKEN']
        print(token)
    except:
        print("a")
        return False

    if token == TOKEN:
        return  True
    else:
        return False

def get_user_token(request):
    # checking whether the user token is there in request
    try:
        user_token = request.META['HTTP_AUTHORIZATION']
    except:
        # if there is no user token, it is a bad request
        print("User token not found in the request.")
        return None
    return user_token

def authenticate_user_token(user_token):
    # call User API to get user ID of the user_token
    try:
        pass
    except:
        return None
    return user_token


# API functions/views

# /drone/create
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_drone(request):
    if not authenticate_api_token(request):
        return Response({"error":unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error":no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # checking the battery parameter was in request
    try:
        battery = request.data['battery']
    except:
        print("Battery not found in request.")
        return Response({"error":no_battery}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # check is request has warehouse for the drone
        warehouse = request.data['warehouse']
        # get id of the warehouse
        warehouse_id = Warehouse.objects.get(name=warehouse)
        if not warehouse_id:
        # if the warehouse does not exist
            return Response({"error": invalid_warehouse}, status=status.HTTP_400_BAD_REQUEST)
    except:
        # warehouse is not passed in the request parameters
        warehouse_id = None

    # save the drone object
    drone = Drone()
    drone.owner = user_id
    drone.battery = battery
    if warehouse_id:
        drone.warehouse = warehouse_id
    drone.save()
    return Response({"success": drone_created}, status=status.HTTP_201_CREATED)


# /drone/list
@api_view(['GET'])
@permission_classes((AllowAny,))
def list_drones(request):
    if not authenticate_api_token(request):
        return Response({"error":unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    # checking parameters one by one
    drones = Drone.objects.all()
    if 'battery' in request.query_params:
        drones = drones.filter(battery=request.query_params['battery'])
    if 'battery_lte' in request.query_params:
        drones = drones.filter(battery__lte=request.query_params['battery_lte'])
    if 'battery_gte' in request.query_params:
        drones = drones.filter(battery__gte=request.query_params['battery_gte'])
    if 'warehouse' in request.query_params:
        warehouse = Warehouse.objects.get(name=request.query_params['warehouse'])
        if warehouse:
            drones = drones.filter(warehouse=warehouse.id)
        else:
            return Response({"error":invalid_warehouse},status=status.HTTP_400_BAD_REQUEST)
    if 'status' in request.query_params:
        if request.query_params['status'] in drone_status:
            drones = drones.filter(status=request.query_params['status'])
        else:
            return Response({"error":invalid_status_choice}, status=status.HTTP_400_BAD_REQUEST)
    return Response(DroneSerializer(drones, many=True).data, status=status.HTTP_200_OK)

# /drone/info
@api_view(['GET'])
@permission_classes((AllowAny,))
def info_drone(request,drone_id):
    if not authenticate_api_token(request):
        return Response({"error":unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # getting the drone
    if(drone_id is None):
        # no drone_id in request
        return Response({"error":no_drone_id}, status=status.HTTP_400_BAD_REQUEST)
    # finding the drone of given ID
    drone = Drone.objects.get(id=drone_id)
    if drone:
        # drone of given ID exists
        return Response(DroneSerializer(drone, many=False).data, status=status.HTTP_200_OK)
    else:
        # drone of given ID does not exist
        return Response({"error":invalid_drone_id}, status=status.HTTP_404_NOT_FOUND)

# /drone/current-battery
@api_view(['GET'])
@permission_classes((AllowAny,))
def current_battery_drone(request,drone_id):
    if not authenticate_api_token(request):
        return Response({"error":unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    if (drone_id is None):
        return Response({"error":no_drone_id}, status=status.HTTP_400_BAD_REQUEST)
    drone = Drone.objects.get(id=drone_id)
    if drone:
        return Response(DroneBatterySerializer(drone, many=False).data, status=status.HTTP_200_OK)
    else:
        return Response({"error": invalid_drone_id}, status=status.HTTP_400_BAD_REQUEST)

# /drone/change-status
@api_view(['PATCH'])
@permission_classes((AllowAny,))
def change_status(request):
    if not authenticate_api_token(request):
        return Response({"error":unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    try:
        drone_id = request.data['drone_id']
    except:
        return Response({"error": no_drone_id}, status=status.HTTP_400_BAD_REQUEST)
    drone = Drone.objects.get(id=drone_id)
    if not drone:
        return Response({"error": invalid_drone_id}, status=status.HTTP_400_BAD_REQUEST)
    try:
        new_status = request.data['status']
    except:
        return Response({"error":no_drone_status}, status=status.HTTP_400_BAD_REQUEST)
    if new_status not in drone_status:
        return Response({"error":invalid_status_choice}, status=status.HTTP_400_BAD_REQUEST)
    drone.status = new_status
    try:
        if request.data['latitude'] and request.data['longitude']:
            drone.curr_latitude = request.data['latitude']
            drone.curr_longitude = request.data['longitude']
    except:
        pass
    drone.save()
    return Response({"success": status_updated}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes((AllowAny,))
def change_location(request):
    if not authenticate_api_token(request):
        return Response({"error":unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    try:
        drone_id = request.data['drone_id']
    except:
        return Response({"error": no_drone_id}, status=status.HTTP_400_BAD_REQUEST)
    drone = Drone.objects.get(id=drone_id)
    if not drone:
        return Response({"error": invalid_drone_id}, status=status.HTTP_400_BAD_REQUEST)
    if drone.status not in ["Delivering", "Returning"]:
        return Response({"error": failed_upadte_location}, status=status.HTTP_400_BAD_REQUEST)
    try:
        if request.data['latitude'] and request.data['longitude']:
            drone.curr_latitude = request.data['latitude']
            drone.curr_longitude = request.data['longitude']
    except:
        return Response({"error": lat_long_missing}, status=status.HTTP_400_BAD_REQUEST)
    drone.save()
    return Response({"success": status_updated}, status=status.HTTP_200_OK)
