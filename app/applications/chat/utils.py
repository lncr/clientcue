import jwt
from django.conf import settings


from applications.chat.models import Notification


def get_connection_token(user):
    user_pk = str(user.pk) if user.is_authenticated else ""
    return jwt.encode({"sub": user_pk}, settings.CENTRIFUGE_SECRET).decode()


def create_notification(title, body, recipient, category=None):
    kwargs_dict = {'title': title, 'body': body, 'recipient': recipient}

    if category:
        kwargs_dict.update({'category': category})
    Notification.objects.create(**kwargs_dict)
