from rest_framework import serializers

from applications.chat.models import Message, ChatRoom, Notification


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'chat_room', 'body', 'file', 'created_at', ]
        read_only_fields = ['sender', 'created_at', ]

    def validate(self, attrs):
        recipients = attrs.get('recipient'), attrs.get('chat_room')

        if all(recipients) or not any(recipients):
            raise serializers.ValidationError('You need to specify either ONLY recipient or ONLY chat_room')

        return attrs


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'created_at', 'title', 'body', 'recipient', ]
        read_only_fields = ['created_at', ]


class ChatRoomSerializer(serializers.ModelSerializer):

    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'team', 'team_name', ]
