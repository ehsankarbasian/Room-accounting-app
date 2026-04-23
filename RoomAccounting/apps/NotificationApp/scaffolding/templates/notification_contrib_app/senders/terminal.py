from typing import Any

from NotificationApp.registry.sender import SenderRegistry
from NotificationApp.interfaces import MessageSenderInterface

from ..message_schema import CanonicalMessage
from ..notification_types import SenderType


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
