from django.apps import AppConfig


class NotificationContribAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.NotificationContribApp"
    
    def ready(self):
        import apps.NotificationContribApp.core.message_sender
