from typing import Dict, Type, Optional, Callable


def make_registry(interface: Optional[Type] = None) -> tuple[Dict[str, Type], Callable]:

    REGISTRY: Dict[str, Type] = {}

    def decorator_to_register(_cls=None, *, name: Optional[str] = None):

        def decorator(cls: Type):
            
            key = name or cls.__name__

            if key in REGISTRY:
                raise RuntimeError(f"{key!r} already registered")

            if interface and not issubclass(cls, interface):
                raise TypeError(
                    f"'{cls.__name__}' must inherit from interface: '{interface.__name__}'"
                )

            REGISTRY[key] = cls
            return cls

        if _cls is None:
            return decorator

        return decorator(_cls)

    return REGISTRY, decorator_to_register
