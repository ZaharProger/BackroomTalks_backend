from django.urls import path
from .views import EnterChatView, DeleteChatView

urlpatterns = [
    path('enter/', EnterChatView.as_view(), name='enter_chat'),
    path('delete/', DeleteChatView.as_view(), name='delete_chat')
]
