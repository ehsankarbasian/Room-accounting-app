"""
Module auto-discovery utility.

Recursively imports all Python modules inside a given package.
Importing these modules allows decorators (such as registry
registrations) to execute at import time.
"""

import importlib
import pathlib


def autodiscover_modules(package_name: str) -> None:
    """
    Import all modules inside the given package recursively.
    """

    package = importlib.import_module(package_name)

    for package_path in package.__path__:
        base_path = pathlib.Path(package_path)

        for file_path in base_path.rglob("*.py"):

            if file_path.name == "__init__.py":
                continue

            relative_path = file_path.relative_to(base_path).with_suffix("")
            module_path = ".".join(relative_path.parts)

            importlib.import_module(f"{package_name}.{module_path}")
