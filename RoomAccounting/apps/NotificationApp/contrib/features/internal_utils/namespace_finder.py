from django.urls import get_resolver, URLResolver, URLPattern


def get_url_namespace(view_url_name):
    
    resolver = get_resolver()
    stack = [resolver]

    while stack:
        current = stack.pop()

        if isinstance(current, URLResolver):
            for pattern in current.url_patterns:
                if isinstance(pattern, URLPattern) and pattern.name == view_url_name:
                    return current.namespace

                if isinstance(pattern, URLResolver):
                    stack.append(pattern)

    return None
