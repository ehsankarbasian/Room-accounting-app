from django.apps import AppConfig


class NotificationAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    
    # In published PyPI packages:
    # name = "NotificationApp"
    # The user will modify it if necessary
    
    name = "apps.NotificationApp"
