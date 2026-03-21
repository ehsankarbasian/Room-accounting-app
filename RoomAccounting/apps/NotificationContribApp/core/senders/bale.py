import requests

from core.settings import BALE_BOT_TOKEN

from apps.NotificationApp.registry import SenderRegistry
from apps.NotificationApp.interfaces import MessageSenderInterface

from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(SenderType.BALE)
class BaleSender(MessageSenderInterface):

    @staticmethod
    def render_payload(message: NotificationCanonicalMessage) -> dict:
        # Converts the canonical NotificationMessage to a Bale-specific payload.

        payload = {
            "text": message.text
        }

        # Bale inline_keyboard:
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
        # Sends the payload to Bale API.
        
        # Add chat_id identifier to payload:
        final_payload = payload.copy()
        final_payload["chat_id"] = identifier
        
        BALE_SEND_MESSAGE_URL = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendMessage"
        
        response = requests.post(url=BALE_SEND_MESSAGE_URL, json=final_payload, timeout=5)
        response.raise_for_status()
