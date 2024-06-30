from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        request_chat_code = self.scope['url_route']['kwargs']['chat_code']
        prepared_chat_code = ''.join([symbol for symbol in request_chat_code \
                                  if not symbol.isdigit()])
        self.chat_name = f'chat_{prepared_chat_code}'

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name
        )

        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            {
                'type': 'chat_message',
                'sender': '',
                'text': '',
                'send_time': ''
            }
        )

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
                'text': request_data['text'],
                'send_time': request_data['send_time']
            }
        )
    
    def chat_message(self, event):
        received_data = json.dumps({
            'sender': event['sender'],
            'text': event['text'],
            'send_time': event['send_time']
        })

        self.send(text_data=received_data)