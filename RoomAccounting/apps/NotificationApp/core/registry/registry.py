from typing import Dict, Type, Optional, Callable

from collections import UserDict
from enum import Enum


class _RegistryDict(UserDict):

    def __init__(self, interface=None):
        super().__init__()
        self.interface = interface

    def __getitem__(self, key):
        
        if key not in self.data:
            if self.interface:
                raise KeyError(
                    f"{key!r} is not registered. "
                    f"You probably forgot to register a "
                    f"{self.interface.__name__} for this key."
                )
                
            raise KeyError(f"{key!r} is not registered.")

        return self.data[key]


def make_registry(interface: Optional[Type] = None) -> tuple[Dict[str, Type], Callable]:

    REGISTRY: Dict[str, Type] = _RegistryDict(interface)

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
