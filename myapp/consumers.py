from channels.generic.websocket import AsyncWebsocketConsumer
import json,os
from django.urls import path
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

active_users = {}


channel_layer = get_channel_layer()

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import waiting_users , UserCommunication
        await self.accept()
        if self.scope['user'].is_authenticated:
            active_users[self.scope["user"].username] = {'channel_name': self.channel_name, 'is_talking': self.scope['user'].is_talking, 'offer': None, 'answer': None}
            exists = await sync_to_async(waiting_users.objects.filter(username=self.scope["user"].username).exists)()
            if not self.scope['user'].is_talking and not exists:
                await sync_to_async(waiting_users.objects.create)(username=self.scope["user"].username)
                print(f'User {self.scope["user"].username} added to waiting_users')
                waiting_users_list = await sync_to_async(list)(waiting_users.objects.values_list('username', flat=True))
                print(waiting_users_list , 'are waiting in connect')
                await self.send_waiting_users()
            await self.send_active_users()
            await self.channel_layer.group_add('active_users_group', self.channel_name)
            await self.send(text_data=json.dumps({
                'username': self.scope['user'].username
            }))

    async def disconnect(self, close_code):
        from .models import waiting_users , UserCommunication
        if self.scope['user'].is_authenticated:
            active_users.pop(self.scope['user'].username, None)
            exists = await sync_to_async(waiting_users.objects.filter(username=self.scope["user"].username).exists)()
            if exists:
                await sync_to_async(waiting_users.objects.filter(username=self.scope["user"].username).delete)()
            await self.send_active_users()
            await self.channel_layer.group_discard('active_users_group', self.channel_name)
    
    async def receive(self, text_data):
        from .models import waiting_users , UserCommunication
        text_data_json = json.loads(text_data)
        d = text_data_json.get('d')
        user = text_data_json.get('user')
        answer = text_data_json.get('answer')
        offer = text_data_json.get('offer')

        user_communication, created = await sync_to_async(UserCommunication.objects.get_or_create)(username=self.scope["user"].username)
        if d is not None:
            user_communication.d = d
        if offer is not None:
            user_communication.offer = offer
        if answer is not None:
            user_communication.answer = answer
        await sync_to_async(user_communication.save)()

        if user_communication.d == 'hola' and await sync_to_async(waiting_users.objects.count)() > 1:
            u1 = await sync_to_async(waiting_users.objects.first)()
            all_users = await sync_to_async(list)(await sync_to_async(waiting_users.objects.all)())
            u2 = all_users[1]
            if u1:
                await sync_to_async(u1.delete)()
            if u2:
                await sync_to_async(u2.delete)()
            waiting_users_list = await sync_to_async(list)(waiting_users.objects.values_list('username', flat=True))
            print(waiting_users_list , 'are waiting')

        user_communication.d = None

        if offer:
            await self.channel_layer.group_send('active_users_group', {
                'type': 'websocket.send',
                'text': json.dumps({'offer' : user_communication.offer})
            })
            user_communication.offer = None
        if answer:
            await self.channel_layer.group_send('active_users_group', {
                'type': 'websocket.send',
                'text': json.dumps({'answer' : user_communication.answer})
            })
            user_communication.answer = None
        await sync_to_async(user_communication.save)()

    async def send_active_users(self):
        from .models import waiting_users , UserCommunication
        active_users_list = [{'username': username, 'is_talking': data['is_talking'], 'offer': data['offer'], 'answer' : data['answer']} for username, data in active_users.items()]
        await self.send(text_data=json.dumps({'active_users': active_users_list}))
        await self.channel_layer.group_send('active_users_group', {'type': 'active_users.update', 'active_users': active_users_list})

    async def active_users_update(self, event):

        active_users_list = event['active_users']
        await self.send(text_data=json.dumps({'active_users': active_users_list}))

    async def send_waiting_users(self):
        from .models import waiting_users , UserCommunication
        waiting_users_list = await sync_to_async(list)(waiting_users.objects.values_list('username', flat=True))
        data = {'waiting_users': waiting_users_list}
        if len(waiting_users_list) >= 1:
            data['user1'] = waiting_users_list[0]
        await self.send(text_data=json.dumps(data))
        await self.channel_layer.group_send('active_users_group', {'type': 'waiting_users.update', 'waiting_users': waiting_users_list})
    
    async def waiting_users_update(self, event):
        from .models import waiting_users , UserCommunication

        waiting_users_list = await sync_to_async(list)(waiting_users.objects.values_list('username', flat=True))
        await self.send(text_data=json.dumps({'waiting_users': waiting_users_list}))

    async def websocket_send(self, event):
        await self.send(event["text"])

websocket_urlpatterns = [
    path('', VideoConsumer.as_asgi()),
]
