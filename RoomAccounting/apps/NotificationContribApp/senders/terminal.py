from typing import Any

from apps.NotificationApp.registry import SenderRegistry
from apps.NotificationApp.interfaces import MessageSenderInterface

from apps.NotificationContribApp.message_schema import CanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.TERMINAL)
class TerminalSender(MessageSenderInterface):
    """
    Development sender that prints notifications to the terminal.

    Useful for debugging and local development environments.
    """


    @staticmethod
    def render_payload(message: CanonicalMessage) -> str:
        """
        Convert CanonicalMessage to a simple text payload.
        """
        return message.text


    @staticmethod
    def send_payload(identifier: Any, payload: str) -> None:
        """
        Print notification payload to terminal.
        """

        print("\n", "-" * 80)

        print("\nSending ...")

        print("\nmessage:")
        print(f"    {payload}")

        print("\nmessage receiver identifier:")
        print(f"    {identifier}")

        print("\n", "-" * 80, "\n")
