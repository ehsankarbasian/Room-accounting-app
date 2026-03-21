import importlib
import pathlib


def autodiscover_modules(package_name):
    package = importlib.import_module(package_name)

    for package_path in package.__path__:
        base_path = pathlib.Path(package_path)

        for file in base_path.rglob("*.py"):
            if file.name == "__init__.py":
                continue

            relative = file.relative_to(base_path).with_suffix("")
            module_path = ".".join(relative.parts)

            importlib.import_module(f"{package_name}.{module_path}")
