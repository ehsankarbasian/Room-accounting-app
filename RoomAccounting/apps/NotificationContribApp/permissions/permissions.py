from apps.NotificationApp.interfaces import PermissionInterface


class LoggedIn(PermissionInterface):
    
    @staticmethod
    def has_permission(recipient):
        return getattr(recipient, "is_authenticated", False)


class NotLoggedIn(PermissionInterface):
    
    @staticmethod
    def has_permission(recipient):
        return not LoggedIn.has_permission(recipient)
