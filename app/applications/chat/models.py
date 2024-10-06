from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatRoom(models.Model):
    team = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True)


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_messages')
    replied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    body = models.TextField(blank=True, default='')
    file = models.FileField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):

    class Category(models.TextChoices):
        INBOX = 'inbox'
        TEAM = 'team'
        REVIEW = 'review'
        EXTRAS = 'extras'

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, blank=True, default='')
    body = models.TextField(blank=True, default='')
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_notifications')
    category = models.CharField(max_length=55, choices=Category.choices, default=Category.EXTRAS)
