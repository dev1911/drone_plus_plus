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

import json
import websocket
from math import sin, cos, sqrt, atan2, radians

# Create your views here.


# reusable functions

ws_url = "ws://127.0.0.1:8000/ws/drone/track/"


def authenticate_api_token(request):
    # checking that this request is from API service
    try:
        token = request.META['HTTP_API_TOKEN']
    except:
        return False
    if token == TOKEN:
        return True
    else:
        return False


def get_user_token(request):
    # checking whether the user token is there in request
    try:
        user_token = request.META['HTTP_USER_TOKEN']
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


def notify_gateway(request, drone_id):
    print("NOFIFY ...............................")
    ws = websocket.create_connection(ws_url + str(drone_id) + '/')
    data = {
        'token': TOKEN,
        'id': drone_id
    }
    try:
        data += {'lat': request.data['latitude']}
        data += {'long': request.data['longitude']}
    except KeyError:
        pass
    try:
        data += {'status': request.data['status']}
    except KeyError:
        pass
    ws.send(json.dumps(data))
    ws.close()


# API functions/views

# /drone/create
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_drone(request):
    if not authenticate_api_token(request):
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # checking the battery parameter was in request
    try:
        battery = request.data['battery']
    except:
        print("Battery not found in request.")
        return Response({"error": no_battery}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
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
            return Response({"error": invalid_warehouse}, status=status.HTTP_400_BAD_REQUEST)
    if 'status' in request.query_params:
        if request.query_params['status'] in drone_status:
            drones = drones.filter(status=request.query_params['status'])
        else:
            return Response({"error": invalid_status_choice}, status=status.HTTP_400_BAD_REQUEST)
    return Response(DroneSerializer(drones, many=True).data, status=status.HTTP_200_OK)


# /drone/info
@api_view(['GET'])
@permission_classes((AllowAny,))
def info_drone(request):
    if not authenticate_api_token(request):
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # getting the drone
    try:
        drone_id = request.query_params['drone_id']
    except:
        # no drone_id in request
        return Response({"error": no_drone_id}, status=status.HTTP_400_BAD_REQUEST)
    # finding the drone of given ID
    drone = Drone.objects.get(id=drone_id)
    if drone:
        # drone of given ID exists
        return Response(DroneSerializer(drone, many=False).data, status=status.HTTP_200_OK)
    else:
        # drone of given ID does not exist
        return Response({"error": invalid_drone_id}, status=status.HTTP_404_NOT_FOUND)


# /drone/current-battery
@api_view(['GET'])
@permission_classes((AllowAny,))
def current_battery_drone(request):
    if not authenticate_api_token(request):
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
    # checking whether the user token is there in request
    user_token = get_user_token(request)
    if not user_token:
        return Response({"error": no_user_token}, status=status.HTTP_400_BAD_REQUEST)
    # call user API to get user-id from user_token
    user_id = authenticate_user_token(user_token)
    if user_id is None:
        return Response({"error": invalid_user_token}, status=status.HTTP_400_BAD_REQUEST)
    try:
        drone_id = request.query_params['drone_id']
    except:
        return Response({"error": no_drone_id}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
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
        return Response({"error": no_drone_status}, status=status.HTTP_400_BAD_REQUEST)
    if new_status not in drone_status:
        return Response({"error": invalid_status_choice}, status=status.HTTP_400_BAD_REQUEST)
    drone.status = new_status
    try:
        if request.data['latitude'] and request.data['longitude']:
            drone.curr_latitude = request.data['latitude']
            drone.curr_longitude = request.data['longitude']
    except:
        pass
    drone.save()
    # notify_gateway(request, drone_id)
    ws = websocket.WebSocket()
    ws.connect(ws_url + str(drone_id) + '/')
    d = {"api_token": TOKEN, "lat": request.data['latitude'], "long": request.data['longitude']}
    ws.send(json.dumps(d))
    ws.close()
    del ws
    return Response({"success": status_updated}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((AllowAny,))
def change_location(request):
    if not authenticate_api_token(request):
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
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
    # notify_gateway(request, drone_id)
    ws = websocket.WebSocket()
    ws.connect(ws_url + str(drone_id) + '/')
    d = {"api_token": TOKEN, "lat": request.data['latitude'], "long": request.data['longitude']}
    ws.send(json.dumps(d))
    ws.close()
    del ws
    return Response({"success": status_updated}, status=status.HTTP_200_OK)


def d(lat1, long1, lat2, long2):
    R = 6373.0
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def get_nearest_warehouse(latitude, longitude):
    warehouses = Warehouse.objects.all()
    min_distance = 10000000000
    closest_warehouse = None
    for warehouse in warehouses:
        distance = d(latitude, longitude, warehouse.latitude, warehouse.longitude)
        if (distance < min_distance):
            min_distance = distance
            closest_warehouse = warehouse
    return closest_warehouse, min_distance


def fifo(latitude, longitude):
    warehouse, min_distance = get_nearest_warehouse(latitude, longitude)
    warehouse_drones = Drone.objects.all().filter(warehouse=warehouse, status="Idle", battery__gte=min_distance)
    if (len(warehouse_drones) <= 0):
        return Response({"error": "Cannot schedule deliveryr right now."}, status=status.HTTP_400_BAD_REQUEST)
    drone = warehouse_drones[0]
    drone.status = "Delivering"
    drone.latitude = warehouse.latitude
    drone.longitude = warehouse.longitude
    drone.save()
    return Response({"success": "Done", "drone_id": drone.id}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def schedule(request):
    if not authenticate_user_token(request):
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
    try:
        latitude = request.data['latitude']
        longitude = request.data['longitude']
        # print("did schedule")
        return fifo(float(latitude), float(longitude))
    except:
        print("could not schedule")
        return Response({'error', 'Failed to schedule delivery. Try again!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def path_(request):
    if not authenticate_user_token(request):
        return Response({"error": unauthorised}, status=status.HTTP_403_FORBIDDEN)
    try:
        warehouse, d = get_nearest_warehouse(float(request.data['lat']), float(request.data['long']))
        return Response({'lat': warehouse.latitude, 'long': warehouse.longitude}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Something went wrong. Try again!'}, status=status.HTTP_400_BAD_REQUEST)