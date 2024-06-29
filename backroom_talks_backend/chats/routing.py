from django.urls import re_path
from .consumers import ChatConsumer


websoket_urlpatterns = [
    re_path(r'^ws/(?P<chat_code>[^/]+)/$', ChatConsumer.as_asgi())
]
