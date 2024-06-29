from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from hashlib import pbkdf2_hmac


class EnterChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response_status = status.HTTP_400_BAD_REQUEST
        response_data = {
            'chat_code': None
        }
  
        if 'seed' in request.data.keys():
            salt = []
            symbol_codes = []
            for symbol in request.data['seed']:
                encoded_symbol = ord(symbol)
                symbol_codes.append(str(encoded_symbol))
                salt.append(encoded_symbol // 2 + len(symbol_codes))

            encoded_seed = ''.join(symbol_codes)

            reversed_seed = ''.join([
                encoded_seed[:len(encoded_seed) // 2],
                encoded_seed[len(encoded_seed) // 2:]
            ])

            hashed_seed = pbkdf2_hmac(
                'sha256',
                reversed_seed.encode('utf-8'),
                salt=bytes(salt),
                iterations=100000,
                dklen=128
            )

            if len(hashed_seed) > 64:
                chat_code = hashed_seed[-1:62:-1].hex()
                client_code = ''.join([str(part) for part in salt])
                client_code = client_code[:len(client_code) // 2]

                response_data['chat_code'] = chat_code
                response_data['chat_code_client'] = client_code
                response_status = status.HTTP_200_OK

        return Response(
            response_data,
            status=response_status,
            content_type='application/json'
        )
