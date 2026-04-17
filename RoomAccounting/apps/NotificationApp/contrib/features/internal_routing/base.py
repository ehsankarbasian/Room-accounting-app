from django.urls import path

from types import FunctionType


def build_feature_path(*, route, view, name: str):
    
    if not name:
        raise ValueError("URL name is required.")

    # Prevent registering a view to multiple URLs
    if hasattr(view, "url_name"):
        raise ValueError(
            f"Feature view '{view.__name__}' is already registered under "
            f"URL name '{view.url_name}'. A feature view may only have one URL."
        )
    
    # Bind url name into view for internal usage using 'django.urls.reverse' function
    view.url_name = name
    
    if not isinstance(view, FunctionType):
        view = view.as_view()

    return path(route, view, name=name)
