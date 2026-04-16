from pathlib import Path

from django.apps import AppConfig
from django.conf import settings


class NotificationAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    
    # In published PyPI packages:
    # name = "NotificationApp"
    # The user will modify it if necessary
    
    name = "apps.NotificationApp"
    
    def ready(self):
        """
        Auto-discover sender modules so they can
        register themselves into the framework registries.
        """

        from apps.NotificationApp.registry.autodiscover import autodiscover_modules
        autodiscover_modules("apps.NotificationApp.contrib.features.internal_features.verification")

        root = Path(__file__).resolve().parent / "contrib/features/internal_features"
        if root.exists():
            feature_templates = [str(p) for p in root.glob("*/templates") if str(p) not in settings.TEMPLATES[0]["DIRS"]]
            settings.TEMPLATES[0]["DIRS"].extend(feature_templates)
