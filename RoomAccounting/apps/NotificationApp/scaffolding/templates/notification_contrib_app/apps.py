from django.apps import AppConfig


class {{ app_config_class }}(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ app_name }}"
    
    def ready(self):
        """
        Auto-discover message and sender modules so they can
        register themselves into the framework registries.
        """

        from apps.NotificationApp.registry.utils import autodiscover_modules

        autodiscover_modules("{{ app_name }}.messages")
        autodiscover_modules("{{ app_name }}.senders")
