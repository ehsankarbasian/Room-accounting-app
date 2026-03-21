from apps.NotificationApp.core.registry import SenderRegistry
from apps.NotificationApp.core.interfaces import MessageSenderInterface

from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.TERMINAL)
class TerminalSender(MessageSenderInterface):

    def render_payload(self, message: NotificationCanonicalMessage) -> str:
        return message.text


    def send_payload(self, payload: dict) -> None:

        print("\n", "-" * 80)

        print("\nSending ...")
        
        print("\nmessage:")
        print(f"    {payload}")

        print("\nmessage reciever identifier:")
        print(f"    {self.identifier}")

        print("\n", "-" * 80, "\n")
