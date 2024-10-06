from django.urls import path
from rest_framework.routers import SimpleRouter

from applications.chat.views import MessageModelViewSet, MessageListView, ChatRoomListView, get_websocket_token

router = SimpleRouter()

router.register('messages', MessageModelViewSet)
router.register('chatrooms', ChatRoomListView)

urlpatterns = [
    path('<int:chat_id>/messages/', MessageListView.as_view({'get': 'list'}), name='chat-message-list'),
    path('ws-token/', get_websocket_token, name='ws-token-url'),
]

urlpatterns += router.urls
