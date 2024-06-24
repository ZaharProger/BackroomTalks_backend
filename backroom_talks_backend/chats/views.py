from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.transaction import atomic


class EnterChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        pass


class DeleteChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request):
        pass
