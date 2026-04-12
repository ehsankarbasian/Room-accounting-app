from django.apps import AppConfig


class NotificationAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    
    # In published PyPI packages:
    # name = "NotificationApp"
    # The user will modify it if necessary
    
    name = "apps.NotificationApp"
    
    def ready(self):
        """
        Auto-discover  sender modules so they can
        register themselves into the framework registries.
        """

        from apps.NotificationApp.registry.autodiscover import autodiscover_modules

        autodiscover_modules("apps.NotificationApp.contrib.features.verification")
