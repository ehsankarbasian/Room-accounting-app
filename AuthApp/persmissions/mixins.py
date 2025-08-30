from django.http import HttpResponse

from AuthApp.persmissions.abstract import _AbstractBasePermission, AbstractPermissionMessage, AbstractPermissionException


class PermissionMixin:
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        for permission in self.permission_classes:
            assert _AbstractBasePermission in permission.__mro__
            
            if not permission.has_permission(request, self):
                if AbstractPermissionMessage in permission.__mro__:
                    message = permission.permission_denied_message
                    return _handle_permission_message(message)
                elif AbstractPermissionException in permission.__mro__:
                    raise permission.permission_denied_exception
        
        return super().dispatch(request, *args, **kwargs)


def _handle_permission_message(message):
    return HttpResponse(f'<h1>{message}</h1>')
