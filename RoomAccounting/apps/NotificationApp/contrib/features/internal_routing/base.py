from django.urls import path

from types import FunctionType


def build_feature_path(*, route, view, name):
    if not name:
        raise ValueError("URL name is required.")

    # Bind url name into view for internal usage if needed
    view.url_name = name
    
    if not isinstance(view, FunctionType):
        view = view.as_view()

    return path(route, view, name=name)
