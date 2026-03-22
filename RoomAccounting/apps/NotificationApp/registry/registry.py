"""
Generic registry system used to register framework components.

Each registry can optionally enforce inheritance from a specific
interface to ensure type safety.
"""

from typing import Dict, Type, Optional, Callable
from collections import UserDict
from enum import Enum


class RegistryDictionary(UserDict):
    """
    Dictionary wrapper providing clearer error messages for missing registrations.
    """

    def __init__(self, interface: Optional[Type] = None):
        super().__init__()
        self._interface = interface

    def __getitem__(self, key):

        if key not in self.data:

            if self._interface:
                raise KeyError(
                    f"{key!r} is not registered. "
                    f"A class implementing {self._interface.__name__} "
                    f"must be registered for this key."
                )

            raise KeyError(f"{key!r} is not registered.")

        return self.data[key]


def make_registry(interface: Optional[Type] = None) -> tuple[Dict[str, Type], Callable]:
    """
    Create a registry and its decorator-based registration function.

    Parameters
        interface: Optional base class that all registered classes must inherit from.

    Returns:
        tuple (registry_dictionary, decorator_function)
    """

    registry_dictionary: Dict[str, Type] = RegistryDictionary(interface)

    def decorator_to_register(name: Enum):

        if not isinstance(name, Enum):
            raise TypeError(
                f"Registry key must be an Enum instance, not {type(name).__name__}"
            )

        def decorator(class_object: Type):

            key = name.value

            if key in registry_dictionary:
                raise RuntimeError(f"{key!r} already registered")

            if interface and not issubclass(class_object, interface):
                raise TypeError(
                    f"{class_object.__name__} must inherit from {interface.__name__}"
                )

            registry_dictionary[key] = class_object
            return class_object

        return decorator

    return registry_dictionary, decorator_to_register
