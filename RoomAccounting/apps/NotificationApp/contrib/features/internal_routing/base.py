from django.urls import path


def build_feature_path(*, route, view, name):
    if not name:
        raise ValueError("URL name is required.")

    # Bind url name into view for internal usage if needed
    view.url_name = name

    return path(route, view, name=name)
