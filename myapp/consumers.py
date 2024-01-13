from channels.generic.websocket import AsyncWebsocketConsumer
import json,os
from django.urls import path
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

channel_layer = get_channel_layer()

class TextConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import waiting_users_text , UserCommunication_text
        if self.scope['user'].is_authenticated:
            await self.accept()
            user_communication = await sync_to_async(UserCommunication_text.get_instance)()
            exists = await sync_to_async(waiting_users_text.objects.filter(username=self.scope["user"].username).exists)()
            if not exists:
                await sync_to_async(waiting_users_text.objects.create)(username=self.scope["user"].username)
                await self.send_waiting_users()
            await self.channel_layer.group_add('text_users_group', self.channel_name)
            if user_communication.offer:
                await self.channel_layer.group_send('text_users_group', {
                    'type': 'websocket.send',
                    'text': json.dumps({'offer' : user_communication.offer})
                })

    async def disconnect(self, close_code):
        from .models import waiting_users_text, UserCommunication_text
        if self.scope['user'].is_authenticated:
            user_communication = await sync_to_async(UserCommunication_text.get_instance)()
            exists = await sync_to_async(waiting_users_text.objects.filter(username=self.scope["user"].username).exists)()
            count = await sync_to_async(waiting_users_text.objects.count)()
            if exists:
                if count < 2:
                    await sync_to_async(UserCommunication_text.objects.all().delete)()
                await sync_to_async(waiting_users_text.objects.filter(username=self.scope["user"].username).delete)()
                print('mf deleted')
            else:
                print('not deleted')

            if user_communication.d == 'hola':
                print('deleted')
                await sync_to_async(UserCommunication_text.objects.all().delete)()

            await self.channel_layer.group_discard('text_users_group', self.channel_name)


    async def receive(self, text_data):
        from .models import waiting_users_text , UserCommunication_text

        text_data_json = json.loads(text_data)
        d = text_data_json.get('d')
        user = text_data_json.get('user')
        answer = text_data_json.get('answer')
        offer = text_data_json.get('offer')
        print('recive activated')
        user_communication = await sync_to_async(UserCommunication_text.get_instance)()
        if d is not None:
            user_communication.d = d
            await sync_to_async(user_communication.save)()

        ice_candidate = text_data_json.get('ice_candidate')
        if ice_candidate:
            user_communication.ice_candidate = ice_candidate
            await sync_to_async(user_communication.save)()

        if offer is not None:
            user_communication.offer = offer
            await sync_to_async(user_communication.save)()
        if answer is not None:
            user_communication.answer = answer
            await sync_to_async(user_communication.save)()

        if user_communication.answer and not user_communication.d:
            await self.send(text_data=json.dumps({'answer': user_communication.answer}))

        if user_communication.offer and not user_communication.d:
            await self.send(text_data=json.dumps({'offer': user_communication.offer}))

        if user_communication.d == 'hola':
            await sync_to_async(UserCommunication_text.objects.all().delete)()

    async def send_waiting_users(self):
        from .models import waiting_users_text , UserCommunication_text
        waiting_users_list = await sync_to_async(list)(waiting_users_text.objects.values_list('username', flat=True))
        data = {'waiting_users': waiting_users_list}
        await self.send(text_data=json.dumps(data))
        await self.channel_layer.group_send('text_users_group', {'type': 'waiting_users.update', 'waiting_users': waiting_users_list})
    
    async def receive_ice_candidate(self, text_data):
        from .models import UserCommunication_text

        text_data_json = json.loads(text_data)
        ice_candidate = text_data_json.get('ice_candidate')

        if ice_candidate:
            user_communication = await sync_to_async(UserCommunication_text.get_instance)()
            user_communication.ice_candidate = ice_candidate
            await sync_to_async(user_communication.save)()
        await self.channel_layer.group_send('text_users_group', {
            'type': 'websocket.send',
            'text': json.dumps({'ice_candidate': user_communication.ice_candidate})
        })


    async def waiting_users_update(self, event):
        from .models import waiting_users_text , UserCommunication_text

        waiting_users_list = await sync_to_async(list)(waiting_users_text.objects.values_list('username', flat=True))
        await self.send(text_data=json.dumps({'waiting_users': waiting_users_list}))

    async def websocket_send(self, event):
        await self.send(event["text"])

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import waiting_users , UserCommunication
        if self.scope['user'].is_authenticated:
            await self.accept()
            user_communication = await sync_to_async(UserCommunication.get_instance)()
            exists = await sync_to_async(waiting_users.objects.filter(username=self.scope["user"].username).exists)()
            if not exists:
                await sync_to_async(waiting_users.objects.create)(username=self.scope["user"].username)
                await self.send_waiting_users()
            await self.channel_layer.group_add('active_users_group', self.channel_name)
            if user_communication.offer:
                await self.channel_layer.group_send('active_users_group', {
                    'type': 'websocket.send',
                    'text': json.dumps({'offer' : user_communication.offer})
                })
            


    async def disconnect(self, close_code):
        from .models import waiting_users, UserCommunication
        if self.scope['user'].is_authenticated:
            user_communication = await sync_to_async(UserCommunication.get_instance)()
            exists = await sync_to_async(waiting_users.objects.filter(username=self.scope["user"].username).exists)()
            count = await sync_to_async(waiting_users.objects.count)()
            if exists:
                if count < 2:
                    await sync_to_async(UserCommunication.objects.all().delete)()
                await sync_to_async(waiting_users.objects.filter(username=self.scope["user"].username).delete)()
                print('mf deleted')
            else:
                print('not deleted')

            if user_communication.d == 'hola':
                print('deleted')
                await sync_to_async(UserCommunication.objects.all().delete)()

            await self.channel_layer.group_discard('active_users_group', self.channel_name)

    async def receive(self, text_data):
        from .models import waiting_users , UserCommunication

        text_data_json = json.loads(text_data)
        d = text_data_json.get('d')
        user = text_data_json.get('user')
        answer = text_data_json.get('answer')
        offer = text_data_json.get('offer')
        print('recive activated')
        user_communication = await sync_to_async(UserCommunication.get_instance)()
        if d is not None:
            user_communication.d = d
            await sync_to_async(user_communication.save)()
        if offer is not None:
            user_communication.offer = offer
            await sync_to_async(user_communication.save)()
        if answer is not None:
            user_communication.answer = answer
            await sync_to_async(user_communication.save)()

        if user_communication.answer and not user_communication.d:
            await self.send(text_data=json.dumps({'answer': user_communication.answer}))

        if user_communication.offer and not user_communication.d:
            await self.send(text_data=json.dumps({'offer': user_communication.offer}))

        if user_communication.d == 'hola':
            await sync_to_async(UserCommunication.objects.all().delete)()

    async def send_waiting_users(self):
        from .models import waiting_users , UserCommunication
        waiting_users_list = await sync_to_async(list)(waiting_users.objects.values_list('username', flat=True))
        data = {'waiting_users': waiting_users_list}
        await self.send(text_data=json.dumps(data))
        await self.channel_layer.group_send('active_users_group', {'type': 'waiting_users.update', 'waiting_users': waiting_users_list})
    
    async def waiting_users_update(self, event):
        from .models import waiting_users , UserCommunication

        waiting_users_list = await sync_to_async(list)(waiting_users.objects.values_list('username', flat=True))
        await self.send(text_data=json.dumps({'waiting_users': waiting_users_list}))

    async def websocket_send(self, event):
        await self.send(event["text"])

class TesttConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import waiting_users_test
        if self.scope['user'].is_authenticated:
            await self.accept()

            await self.channel_layer.group_add('active_users_group', self.channel_name)


    async def disconnect(self, close_code):
        from .models import waiting_users_test
        if self.scope['user'].is_authenticated:

            exists = await sync_to_async(waiting_users_test.objects.filter(username=self.scope["user"].username).exists)()
            if exists:
                await sync_to_async(waiting_users_test.objects.filter(username=self.scope["user"].username).delete)()
                print('mf deleted')
            else:
                print('not deleted')

            await self.channel_layer.group_discard('active_users_group', self.channel_name)

    async def receive(self, text_data):
        from .models import waiting_users_test
        text_data_json = json.loads(text_data)
        duser = text_data_json.get('peer')
        dusername = duser.get('username')
        dpeer_id = duser.get('peer_id')

        if dpeer_id:
            user_test, created = await sync_to_async(waiting_users_test.objects.get_or_create)(username=dusername)
            user_test.peer_id = dpeer_id
            await sync_to_async(user_test.save)()

            waiting_users = await sync_to_async(list)(waiting_users_test.objects.all().values('username', 'peer_id'))
            
            # Send information of both waiting users to the group
            await self.channel_layer.group_send(
                'active_users_group',
                {
                    'type': 'group.message',
                    'users': waiting_users  # Send the list of waiting users
                }
            )





    async def group_message(self, event):
        await self.send(text_data=json.dumps(event))

class TesttvideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.accept()

            await self.channel_layer.group_add('video_user_group', self.channel_name)


    async def disconnect(self, close_code):
        from .models import waiting_users_test_video
        if self.scope['user'].is_authenticated:

            exists = await sync_to_async(waiting_users_test_video.objects.filter(username=self.scope["user"].username).exists)()
            if exists:
                await sync_to_async(waiting_users_test_video.objects.filter(username=self.scope["user"].username).delete)()
                print('mf deleted')
            else:
                print('not deleted')

            await self.channel_layer.group_discard('video_user_group', self.channel_name)

    async def receive(self, text_data):
        from .models import waiting_users_test_video
        text_data_json = json.loads(text_data)
        duser = text_data_json.get('peer')
        dusername = duser.get('username')
        dpeer_id = duser.get('peer_id')

        if dpeer_id:
            user_test, created = await sync_to_async(waiting_users_test_video.objects.get_or_create)(username=dusername)
            user_test.peer_id = dpeer_id
            await sync_to_async(user_test.save)()

            waiting_users = await sync_to_async(list)(waiting_users_test_video.objects.all().values('username', 'peer_id'))
            
            # Send information of both waiting users to the group
            await self.channel_layer.group_send(
                'video_user_group',
                {
                    'type': 'group.message',
                    'users': waiting_users  # Send the list of waiting users
                }
            )





    async def group_message(self, event):
        await self.send(text_data=json.dumps(event))


class shit(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

websocket_urlpatterns = [
    path('video/', VideoConsumer.as_asgi()),
    path('text/', TextConsumer.as_asgi()),
    path('testt/', TesttConsumer.as_asgi()),
    path('testtvideo/', TesttvideoConsumer.as_asgi()),
    path('shit/', shit.as_asgi()),
]