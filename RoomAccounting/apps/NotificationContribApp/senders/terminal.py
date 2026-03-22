from typing import Any

from apps.NotificationApp.registry import SenderRegistry
from apps.NotificationApp.interfaces import MessageSenderInterface

from apps.NotificationContribApp.messages.canonical import CanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.TERMINAL)
class TerminalSender(MessageSenderInterface):

    @staticmethod
    def render_payload(message: CanonicalMessage) -> str:
        return message.text


    @staticmethod
    def send_payload(identifier: Any, payload: dict) -> None:

        print("\n", "-" * 80)

        print("\nSending ...")
        
        print("\nmessage:")
        print(f"    {payload}")

        print("\nmessage reciever identifier:")
        print(f"    {identifier}")

        print("\n", "-" * 80, "\n")
