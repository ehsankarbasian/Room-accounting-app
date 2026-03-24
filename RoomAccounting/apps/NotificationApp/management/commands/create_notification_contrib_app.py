import shutil
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.template import Context, Engine


class Command(BaseCommand):
    help = "Create a Notification Contrib app skeleton."

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            type=str,
            help="Name of the contrib app",
        )

    def handle(self, *args, **options):
        app_name = options["name"]

        target_dir = Path.cwd() / app_name

        if target_dir.exists():
            raise CommandError(f"Directory '{app_name}' already exists.")

        template_dir = (
            Path(__file__)
            .resolve()
            .parents[3]
            / "NotificationApp"
            / "contrib_template"
            / "notification_contrib_app"
        )

        if not template_dir.exists():
            raise CommandError("Template directory not found.")

        self.stdout.write(f"Creating notification contrib app '{app_name}'...")

        shutil.copytree(template_dir, target_dir)

        context = self.build_context(app_name)

        self.render_templates(target_dir, context)

        self.stdout.write(
            self.style.SUCCESS(
                f"Notification contrib app '{app_name}' created successfully."
            )
        )

        self.stdout.write(
            f"\nAdd '{app_name}' to INSTALLED_APPS to activate it."
        )

    def build_context(self, app_name):
        return {
            "app_name": app_name,
            "app_config_class": f"{app_name.capitalize()}Config",
        }

    def render_templates(self, directory: Path, context_dict):
        engine = Engine()
        context = Context(context_dict)

        for file_path in directory.rglob("*"):

            if not file_path.is_file():
                continue

            content = file_path.read_text()

            template = engine.from_string(content)

            rendered = template.render(context)

            file_path.write_text(rendered)
