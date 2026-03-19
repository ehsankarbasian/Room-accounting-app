from django.apps import AppConfig




class NotificationContribAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.NotificationContribApp"
    
    def ready(self):
        from apps.NotificationApp.core.registry.autodiscover import autodiscover_modules
        
        autodiscover_modules("apps.NotificationContribApp.core")
