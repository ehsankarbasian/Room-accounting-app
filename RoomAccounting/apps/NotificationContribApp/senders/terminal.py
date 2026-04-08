from typing import Any

from apps.NotificationApp.interfaces import MessageSenderInterface
from apps.NotificationContribApp.message_schema import CanonicalMessage


class TerminalSender(MessageSenderInterface):
    """
    Development sender that prints notifications to the terminal.

    Useful for debugging and local development environments.
    """

    sender_key = "terminal"
    
    @staticmethod
    def render_payload(message: CanonicalMessage) -> str:
        """
        Convert CanonicalMessage to a simple text payload.
        """
        
        result_begin = 40*"#" + " Message Begin " + 40*"#"
        result_end = 41*"#" + " Message End " + 41*"#"
        
        result = f"message_text:\n{message.text}"
        
        if message.buttons:
            result += "\n\n" + 35*"-" + " Buttons " + 35*"-" + "\n"
        for button in message.buttons:
            result += f"\n{button.text}:\n{button.target}\n"
            
        if message.button_links:
            result += "\n\n" + 35*"-" + " Button Links " + 35*"-" + "\n"
        for link in message.button_links:
            result += f"\n{link.text}:\n{link.target}\n"
            
        return f"{result_begin}\n\n{result}\n\n{result_end}"


    @staticmethod
    def send_payload(identifier: Any, payload: str) -> None:
        """
        Print notification payload to terminal.
        """

        print("\n", "-" * 100)
        print("\nSending ...\n")

        print(payload)

        print("\nmessage receiver identifier:")
        print(f"    {identifier}")

        print("\n", "-" * 100, "\n")
