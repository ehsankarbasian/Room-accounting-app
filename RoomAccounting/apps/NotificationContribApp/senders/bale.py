import requests

from core.settings import BALE_BOT_TOKEN

from apps.NotificationApp.registry import SenderRegistry
from apps.NotificationApp.interfaces import MessageSenderInterface

from apps.NotificationContribApp.messages.canonical import CanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.BALE)
class BaleSender(MessageSenderInterface):
    """
    Sender implementation for Bale messenger bot API.
    """

    @staticmethod
    def render_payload(message: CanonicalMessage) -> dict:
        """
        Convert CanonicalMessage into Bale API payload.
        """

        payload = {
            "text": message.text
        }

        if message.buttons:
            payload["reply_markup"] = {
                "inline_keyboard": [
                    [
                        {
                            "text": btn.text,
                            "url": btn.target
                        }
                    ]
                    for btn in message.buttons
                ]
            }

        return payload


    @staticmethod
    def send_payload(identifier: int, payload: dict) -> None:
        """
        Send message using Bale bot API.
        """

        final_payload = payload.copy()
        final_payload["chat_id"] = identifier

        url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendMessage"

        response = requests.post(
            url=url,
            json=final_payload,
            timeout=5,
        )

        response.raise_for_status()
