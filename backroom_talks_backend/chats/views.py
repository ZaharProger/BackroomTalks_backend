from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import hashlib
from uuid import uuid4

from .models import Chat


class EnterChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response_status = status.HTTP_400_BAD_REQUEST
        response_data = {
            'chat_code': None
        }
  
        if 'seed' in request.data.keys():
            encoded_seed = ''.join([str(ord(symbol)) for symbol in request.data['seed']])
            reversed_seed = ''.join([
                encoded_seed[:len(encoded_seed) // 2],
                encoded_seed[len(encoded_seed) // 2:]
            ])

            hashed_seed = hashlib.pbkdf2_hmac(
                'sha256',
                reversed_seed.encode('utf-8'),
                salt=os.urandom(32),
                iterations=100000,
                dklen=128
            )

            if len(hashed_seed) > 64:
                chat_code = hashed_seed[-1:62:-1]
                Chat.objects.create(code=chat_code).save()
                response_data['chat_code'] = chat_code.decode('latin-1').replace("'", '"')
                response_data['chat_code_client'] = uuid4().hex
                response_status = status.HTTP_200_OK

        return Response(
            response_data,
            status=response_status,
            content_type='application/json'
        )


class DeleteChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request):
        response_status = status.HTTP_400_BAD_REQUEST

        if 'chat_code' in request.data.keys():
            chat_code = request.data['chat_code']
            Chat.objects.filter(code=chat_code).delete()
            response_status = status.HTTP_200_OK
        
        return Response(
            {},
            status=response_status,
            content_type='application/json'
        )
