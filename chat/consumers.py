# chat/consumers.py
import json

import channels.layers
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import plan


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % user.username

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('connected to room')
        print(self.channel_layer)
        print(self.channel_name)
        print(self.channel_layer.group_add)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(close_code)
        print('disconnected')

    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print('received')


    def chat_message(self, event):

        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

        print('chat_message function called')
        print('event'+str(event))

    @receiver(post_save, sender=plan, dispatch_uid="only_plan_stuff")
    def update_stock(sender, instance, **kwargs):
        message = {
            'job_id': instance.plan_name,
            'title': instance.plan_id,
            'status': instance.users,
            'modified': instance.devices,

        }

        channel_layer = channels.layers.get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'chat_message',
                'text': message
            }
        )


