from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.chat'

    def ready(self):
        import applications.chat.signals
