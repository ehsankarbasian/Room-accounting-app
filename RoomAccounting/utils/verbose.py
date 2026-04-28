from core.settings import ADMIN_PRIORITY


def verbose_name_plural(model_name):
    for model in ADMIN_PRIORITY:
        if model_name in model:
            return ' ' * ADMIN_PRIORITY[::-1].index(model_name) + model_name
    return 'ERROR: TABLE NAME NOT FOUND IN settings'
