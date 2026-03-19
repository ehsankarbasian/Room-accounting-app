from typing import Dict, Type, Optional, Callable
from enum import Enum


def make_registry(interface: Optional[Type] = None) -> tuple[Dict[str, Type], Callable]:

    REGISTRY: Dict[str, Type] = {}

    def decorator_to_register(_cls=None, *, name: Optional[Enum] = None):

        def decorator(cls: Type):

            if name is None:
                raise TypeError("Registry key must be provided via 'name' using an Enum value")

            if not isinstance(name, Enum):
                raise TypeError(
                    f"Registry key must be an Enum instance, not {type(name).__name__}"
                )

            key = name.value

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
