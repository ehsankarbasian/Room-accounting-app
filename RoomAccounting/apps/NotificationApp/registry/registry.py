
class SenderRegistry:
    _registry = {}

    @classmethod
    def register(cls, key, sender_class):
        if key in cls._registry:
            raise ValueError(f"Duplicate sender key: {key}")
        cls._registry[key] = sender_class

    @classmethod
    def get(cls, key):
        return cls._registry.get(key)
