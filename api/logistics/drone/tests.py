from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
import json
from drone.models import *
from logistics.msgs import *
from drone.serializers import *
# Create your tests here.

header = {"HTTP_USER_TOKEN": "admin"}

class CreateDroneTest(APITestCase):

    ######################
    # CREATE DRONE TESTS #
    ######################

    # success tests
    def test_drone_create_0(self):
        """
        Ensure we can create a drone when warehouse is not passed
        """
        url = reverse('create_drone')
        data = {"battery": "5.0"}
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drone.objects.count(), 1)
        self.assertEqual(json.loads(response.content), {"success": drone_created})

    def test_create_drone_1(self):
        """
        Ensure we can create a drone when warehouse is passed
        """
        url = reverse('create_drone')
        data = {"battery":"5.0", "warehouse": "Testing Drones Pvt Ltd"}
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drone.objects.count(),1)
        self.assertEqual(json.loads(response.content), {"success": drone_created})

    # failure tests
    def test_create_drone_2(self):
        """
        Failure tests when battery is not passed
        """
        url = reverse('create_drone')
        data = {}
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Drone.objects.count(), 0)
        self.assertEqual(json.loads(response.content), {"error": no_battery})

    def test_create_drone_3(self):
        """
        Failure test when user_token is not passed
        """
        url = reverse('create_drone')
        data = {"battery":"5.0"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Drone.objects.count(), 0)
        self.assertEqual(json.loads(response.content), {"error": no_user_token})


class InfoDroneTest(APITestCase):

    ####################
    # INFO DRONE TESTS #
    ####################

    def setUp(self):
        Drone.objects.create(owner="admin", battery=5.0, curr_battery=5.0, status="Idle")
        # Drone.objects.create(owner="admin", battery=5.0)

    # success tests
    def test_info_0(self):
        """
        Ensure that drone info can be received
        """
        url = reverse('info_drone')
        data = {"drone_id":1}
        response = self.client.get(url, data=data, format='json', **header)
        # TODO: need fix
        self.assertEqual(json.loads(response.content), {"id":1,"owner":"admin", "battery":5.0, "curr_battery":5.0, "status":"Idle", "curr_latitude":None, "curr_longitude":None, "warehouse":None})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drone.objects.count(), 1)


class CurrentBatteryTest(APITestCase):

    #########################
    # CURRENT BATTERY TESTS #
    #########################

    def setUp(self):
        self.drone = Drone.objects.create(owner="admin", battery=5.0, curr_battery=5.0, status="Idle")

    # success tests
    def test_current_battery_0(self):
        """
        Ensure that current battery is returned
        """
        url = reverse('current_battery_drone')
        data = {"drone_id": 1}
        response = self.client.get(url, data, format='json', **header)
        self.assertEqual(json.loads(response.content), DroneBatterySerializer(self.drone).data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drone.objects.count(), 1)

    # failure tests
    def test_current_battery_1(self):
        """
        Failure when no drone_id was passed in params
        """
        url = reverse('current_battery_drone')
        data = {}
        response = self.client.get(url, data, format='json', **header)
        self.assertEqual(json.loads(response.content), {"error":no_drone_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Drone.objects.count(), 1)

class ChangeStatusDroneTesr(APITestCase):

    #######################
    # CHANGE STATUS TESTS #
    #######################

    def setUp(self):
        self.drone = Drone.objects.create(owner="admin", battery=5.0, curr_battery=5.0, status="Idle")

    # success tests
    def test_change_status_0(self):
        """
        Ensures that the drone status can be changed
        """
        url = reverse('change_status')
        data = {"drone_id": 1, "status":"Charging"}
        response = self.client.patch(url, data, format='json', **header)
        self.assertEqual(json.loads(response.content), {"success":status_updated})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drone.objects.count(), 1)

    def test_change_status_1(self):
        """
        Ensures that the drone status can be changed with lat and long
        """
        url = reverse('change_status')
        data = {"drone_id": 1, "status": "Charging", "latitude":18.9771, "longitude":72.8342}
        response = self.client.patch(url, data, format='json', **header)
        self.assertEqual(json.loads(response.content), {"success": status_updated})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drone.objects.count(), 1)

    # failure cases
    def test_change_status_2(self):
        """
        Failed case when status is bad arg
        """
        url = reverse('change_status')

        data = {"drone_id": 1, "status": "Apple"}
        response = self.client.patch(url, data, format='json', **header)
        self.assertEqual(json.loads(response.content), {"error":invalid_status_choice})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_status_3(self):
        """
        Failed case when status is not passed
        """
        url = reverse('change_status')
        data = {"drone_id": 1}
        response = self.client.patch(url, data, format='json', **header)
        self.assertEqual(json.loads(response.content), {"error":no_drone_status})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
