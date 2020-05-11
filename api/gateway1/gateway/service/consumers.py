from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from gateway.msgs import *

class DroneTrackConsumer(WebsocketConsumer):
    def connect(self):
        self.drone_id = self.scope['url_route']['kwargs']['drone_id']
        self.group_name = 'drone_track%s' % self.drone_id
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        try:
            if(text_data['api_token'] != TOKEN):
                return
            lat = text_data['lat']
            long = text_data['long']
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'location',
                    'lat': lat,
                    'long': long
                }
            )
        except:
            raise ValueError("RECEIVE PROBLEM")

    def location(self, event):
        lat = event['lat']
        long = event['long']
        self.send(text_data=json.dumps(
            {
                'lat':lat,
                'long':long
            }
        ))
