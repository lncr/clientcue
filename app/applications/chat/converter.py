from datetime import datetime
from applications.chat.models import Message, Notification


def message_from_obj_to_dict(message: Message) -> dict:
    """
    Converts Message object into dictionary to publish via WebSocket
    """
    result_dict = {
        'id': message.id,
        'sender': message.sender_id,
        'recipient': message.recipient_id,
        'replied_to': message.replied_to_id,
        'chat': message.chat_room_id,
        'body': message.body,
        'file': message.file.url if message.file else None,
        'created_at': datetime.strftime(message.created_at, '%Y.%m.%d %H:%M')
    }
    return result_dict


def notification_from_obj_to_dict(notification: Notification):
    """
    Converts Notification object into dictionary to publish via WebSocket
    """
    result_dict = {
        'id': notification.id,
        'title': notification.title,
        'body': notification.body,
        'recipient': notification.recipient_id,
        'created_at': datetime.strftime(notification.created_at, '%Y.%m.%d %H:%M')
    }

    return result_dict
