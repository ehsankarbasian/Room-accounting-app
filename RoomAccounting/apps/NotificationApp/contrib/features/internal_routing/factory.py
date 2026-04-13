from .base import build_feature_path


def make_feature_path(*, view, default_route):
    """
    Produces a public-facing path function for a feature, without code duplication.
    """
    
    def _factory(route=default_route, *, name):
        
        return build_feature_path(
            route=route,
            view=view,
            name=name,
        )
        
    return _factory
