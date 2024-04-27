from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from chat.models import GroupMember, UserGroup, GroupMessage
from dashboard.models import OnlineMember
from datetime import datetime
from django.contrib.auth import get_user_model

from studyhive.settings import hate_speech_detection

class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = set()

    @database_sync_to_async
    def insert_message(self, message, upload, group):
        print("inserting.......")
        try:
            member = GroupMember.objects.get(member=self.scope["user"], group=self.group)
            GroupMessage.objects.create(
                member=member,
                message=message,
                group=group,
                upload=upload
            )

        except Exception as e:
            print(e)

    @database_sync_to_async
    def get_group(self, group_id):
        try:
            return UserGroup.objects.get(uid=group_id)

        except UserGroup.DoesNotExist:
            return None

    @database_sync_to_async
    def group_call(self, on_call):
        self.group.on_call = on_call
        self.group.save()

    @database_sync_to_async
    def online_user(self, status, group):
        try:
            member = GroupMember.objects.filter(member=self.scope["user"], group=group).update(online=status)
            online, created = OnlineMember.objects.get_or_create(member=member, date=datetime.now().date())

        except Exception as e:
            pass

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.group = await self.get_group(self.room_name)

        if self.group is None:
            await self.close()
            return

        if len(self.connected_users) == 0:
            await self.group_call(False)
        
        self.connected_users.add(self.scope["user"])
        await self.online_user(True, self.group)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.online_user(False, self.group)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.connected_users.remove(self.scope["user"])
        if len(self.connected_users) == 0:
            await self.group_call(False)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        upload = None

        if "upload" in data:
            upload = data['upload']

        member = self.scope["user"]

        if "type" in data:
            if data['type'] == "voice":
                print("voice chat active")
                await self.group_call(data['message'])
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'voice',
                        'message': message,
                        'member': member,
                        'date': str(datetime.now()),
                        'upload': upload
                    }
                )
            else:
                prediction = hate_speech_detection(message)
                if prediction:
                    message = f"This message has been flagged as {prediction}"

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'member': {
                            "username" : member.username,
                            "id" : str(member.id)
                        },
                        'date': str(datetime.now()),
                        'upload': upload
                    }
                )

                await self.insert_message(message, upload, self.group)

    async def chat_message(self, event):
        message = event['message']
        member = event['member']
        date = event['date']
        chat_type = event["type"]

        await self.send(
            text_data=json.dumps({
                'type': chat_type,
                'message': message,
                'member': member,
                'date': date,
            })
        )

    # async def voice(self, event):
    #     message = event['message']
    #     member = event['member']
    #     date = event['date']
    #     upload = event['upload']

    #     await self.send(
    #         text_data=json.dumps({
    #             'type': 'voice',
    #             'message': message,
    #             'member': member,
    #             'date': date,
    #             'upload': upload
    #         })
    #     )
