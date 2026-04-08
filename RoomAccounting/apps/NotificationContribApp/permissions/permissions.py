from apps.NotificationApp.interfaces import PermissionInterface


class LoggedIn(PermissionInterface):
    
    @staticmethod
    def has_permission(recipient, *, channel):
        return getattr(recipient, "is_authenticated", False)


class NotLoggedIn(PermissionInterface):
    
    @staticmethod
    def has_permission(recipient, *, channel):
        return not LoggedIn.has_permission(recipient, channel=channel)
