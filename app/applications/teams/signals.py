from django.db.models.signals import post_save
from django.dispatch import receiver


from applications.teams.models import Team
from applications.chat.models import ChatRoom


@receiver(post_save, sender=Team)
def create_chatroom_for_team(sender, instance, created, **kwargs):
    if created:
        ChatRoom.objects.create(team=instance)
