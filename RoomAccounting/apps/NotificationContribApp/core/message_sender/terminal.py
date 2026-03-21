from apps.NotificationApp.core.registry import SenderRegistry
from apps.NotificationApp.core.interfaces import MessageSenderInterface
from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage

from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(name=SenderType.TERMINAL)
class TerminalSender(MessageSenderInterface):

    def __init__(self, identifier):
        self._to = identifier

    def render_payload(self, message: NotificationCanonicalMessage):
        return message.text

    def send(self, payload):

        print("\n", "-" * 80)

        print("\nSending ...")
        
        print("\nmessage:")
        print(f"    {payload}")

        print("\nmessage reciever identifier:")
        print(f"    {self._to}")

        print("\n", "-" * 80, "\n")
