from django.db.models.signals import post_save
from django.dispatch import receiver


from applications.chat.models import Message, Notification
from applications.chat.agents import CentrifugoAgent
from applications.chat.converter import message_from_obj_to_dict, notification_from_obj_to_dict


@receiver(post_save, sender=Message)
def send_ws_messages(sender, instance, created, **kwargs):
    if created:
        centrifugo_agent = CentrifugoAgent()
        message_dict = message_from_obj_to_dict(instance)
        if instance.recipient:
            centrifugo_agent.publish(
                channel=f'user_{instance.recipient_id}',
                message=message_dict
            )
            centrifugo_agent.publish(
                channel=f'user_{instance.sender_id}',
                message=message_dict
            )
        else:
            roles = instance.chat_room.team.roles.all()
            if roles:
                agents = roles[0].agents.all()
                for i in range(1, roles.count()):
                    agents |= roles[i].agents.all()
                user_ids = [agent.user_id for agent in agents]
            else:
                user_ids = []
            params_list = [{'channel': f'user_{user_id}', 'data': f'{message_dict}'} for user_id in user_ids]
            centrifugo_agent.publish_multiple(params_list=params_list)


@receiver(post_save, sender=Notification)
def send_ws_notifications(sender, instance, created, **kwargs):
    if created:
        centrifugo_agent = CentrifugoAgent()
        notification_dict = notification_from_obj_to_dict(instance)
        centrifugo_agent.publish(
            channel=f'notification_{instance.recipient_id}',
            message=notification_dict
        )
