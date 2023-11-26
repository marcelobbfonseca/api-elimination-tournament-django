import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotifyVoteConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # validate connection here
        self.group_name = 'position_vote'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    # receive message from websocket {'positionId': '2'}
    async def receive(self, text_data):
        # sends message to group
        event = {
            'type': 'send_message',
            'text': text_data
        }
        await self.channel_layer.group_send(self.group_name, event)

    # receive message from group
    async def send_message(self, event):
        # send message to websocket
        await self.send(text_data=event['text'])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
