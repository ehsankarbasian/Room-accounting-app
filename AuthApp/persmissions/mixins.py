
class PermissionMixin:
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        for permission in self.permission_classes:
            if not permission.has_permission(request, self):
                raise permission.permission_denied_exception
        return super().dispatch(request, *args, **kwargs)
