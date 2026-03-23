from django.apps import AppConfig


class NotificationContribAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.NotificationContribApp"
    
    def ready(self):
        """
        Auto-discover message and sender modules so they can
        register themselves into the framework registries.
        """

        from apps.NotificationApp.registry.autodiscover import autodiscover_modules

        autodiscover_modules("apps.NotificationContribApp.messages")
        autodiscover_modules("apps.NotificationContribApp.senders")
