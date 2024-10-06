from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from applications.chat.models import Message, ChatRoom, Notification
from applications.chat.permissions import MessageDetailPermission
from applications.chat.serializers import MessageSerializer, ChatRoomSerializer, NotificationSerializer
from applications.chat.utils import get_connection_token


class MessageModelViewSet(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | MessageDetailPermission, ]

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(sender=user)


class MessageListView(ListModelMixin, GenericViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        return self.queryset.filter(chat_id=chat_id).order_by('-id')


class ChatRoomListView(ListModelMixin, GenericViewSet):

    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        agents = user.agents.all()
        roles = agents[0].roles.all()
        for i in range(1, agents.count()):
            roles |= agents[0].roles.all()
        team_ids = {role.team_id for role in roles}
        for team in user.teams.all():
            team_ids.add(team.id)
        return self.queryset.filter(team_id__in=team_ids).order_by('-id')


class NotificationListView(ListModelMixin, GenericViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(recipient_id=user.id).order_by('-id')


@api_view
@permission_classes([IsAuthenticated, ])
def get_websocket_token(request):
    token = get_connection_token(request.user)
    return Response({"token": token})
