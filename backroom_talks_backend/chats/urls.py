from django.urls import path
from .views import EnterChatView

urlpatterns = [
    path('enter/', EnterChatView.as_view(), name='enter_chat')
]
