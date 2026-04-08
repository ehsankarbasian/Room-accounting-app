from django.conf import settings
from django.utils.module_loading import import_string


_DEFAULT_TOKEN_GENERATOR = "apps.NotificationApp.contrib.tokens.default.NumericSixDigitTokenGenerator"


def _get_token_generator():
    path = getattr(settings, "NOTIFICATION_TOKEN_GENERATOR", _DEFAULT_TOKEN_GENERATOR)
    class_ = import_string(path)
    return class_


TokenGenerator = _get_token_generator()
