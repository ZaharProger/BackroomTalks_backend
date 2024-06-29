from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_code = self.scope['url_route']['kwargs']['chat_code']
        self.chat_name = f'channel{self.chat_code}'

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        request_data = json.loads(text_data)
        
        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            {
                'type': 'chat_message',
                'sender': request_data['sender'],
                'message': request_data['message']
            }
        )
    
    def chat_message(self, event):
        received_data = json.dumps({
            'sender': event['sender'],
            'message': event['message']
        })

        self.send(text_data=received_data)