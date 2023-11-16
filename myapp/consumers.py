from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.urls import path
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import logging
logging.info('سلام')

active_users = {}
waiting_users = []
channel_layer = get_channel_layer()

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        if self.scope['user'].is_authenticated:
            active_users[self.scope["user"].username] = {'channel_name': self.channel_name, 'is_talking': self.scope['user'].is_talking, 'offer': None, 'answer': None}
            if not self.scope['user'].is_talking:
                waiting_users.append(self.scope["user"].username)
                print(f'User {self.scope["user"].username} added to waiting_users')
                await self.send_waiting_users()
            await self.send_active_users()
            await self.channel_layer.group_add('active_users_group', self.channel_name)
            await self.send(text_data=json.dumps({
                'username': self.scope['user'].username
            }))

    async def disconnect(self, close_code):
        if self.scope['user'].is_authenticated:
            del active_users[self.scope['user'].username]
            if self.scope["user"].username in waiting_users:
                waiting_users.remove(self.scope["user"].username)
                print(f'User {self.scope["user"].username} removed from waiting_users')
            await self.send_active_users()
            await self.channel_layer.group_discard('active_users_group', self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        d = text_data_json.get('d')
        user = text_data_json.get('user')
        answer = text_data_json.get('answer')
        offer = text_data_json.get('offer')
        print(d)
        if d == 'hola' :
            u1 = waiting_users[0]
            u2 = waiting_users[1]
            waiting_users.remove(u1)
            waiting_users.remove(u2)
        print('wait' ,waiting_users)


        
        if offer:
            await self.channel_layer.group_send('active_users_group', {
                'type': 'websocket.send',
                'text': json.dumps({'offer' : offer})
            })
        offer = None
        print(offer)
        if answer:
            await self.channel_layer.group_send('active_users_group', {
                'type': 'websocket.send',
                'text': json.dumps({'answer' : answer})
            })
        answer = None
        print(answer)
        if self.scope['user'].is_authenticated and self.scope['user'].username in waiting_users and active_users[self.scope['user'].username]['is_talking']:
            waiting_users.remove(self.scope['user'].username)
            await self.send_waiting_users()

    async def send_active_users(self):
        active_users_list = [{'username': username, 'is_talking': data['is_talking'], 'offer': data['offer'], 'answer' : data['answer']} for username, data in active_users.items()]
        await self.send(text_data=json.dumps({'active_users': active_users_list}))
        await self.channel_layer.group_send('active_users_group', {'type': 'active_users.update', 'active_users': active_users_list})

    async def active_users_update(self, event):
        active_users_list = event['active_users']
        await self.send(text_data=json.dumps({'active_users': active_users_list}))

    async def send_waiting_users(self):
        print(f'Sending waiting users: {waiting_users}')
        data = {
            'waiting_users': waiting_users
        }
        
        if len(waiting_users) >= 1:
            data['user1'] = waiting_users[0]

        await self.send(text_data=json.dumps(data))
        await self.channel_layer.group_send('active_users_group', {'type': 'waiting_users.update', 'waiting_users': waiting_users})
        
    async def waiting_users_update(self, event):
        waiting_users_list = event['waiting_users']
        await self.send(text_data=json.dumps({'waiting_users': waiting_users_list}))

    async def websocket_send(self, event):
        await self.send(event["text"])

websocket_urlpatterns = [
    path('', VideoConsumer.as_asgi()),
]
