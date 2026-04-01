from apps.NotificationApp.interfaces import MessageSenderInterface


class SmsSender(MessageSenderInterface):
    """
    This is currently a placeholder and should be implemented
    using an SMS provider.
    """
    
    sender_key = "sms"
