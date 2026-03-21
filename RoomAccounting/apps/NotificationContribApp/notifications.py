from apps.NotificationApp.core.registry.autodiscover import autodiscover_modules

autodiscover_modules(__name__)


from apps.NotificationApp.core.registry import MapperRegistry, DataModelRegistry

if set(MapperRegistry.REGISTRY) != set(DataModelRegistry.REGISTRY):
    raise RuntimeError(
        "MapperRegistry and DataModelRegistry are inconsistent"
    )
