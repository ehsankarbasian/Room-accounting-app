import requests

from core.settings import BALE_BOT_TOKEN

from apps.NotificationApp.interfaces import MessageSenderInterface
from apps.NotificationContribApp.message_schema import CanonicalMessage


class BaleSender(MessageSenderInterface):
    """
    Sender implementation for Bale messenger bot API.
    """
    
    sender_key = "bale"
    
    @staticmethod
    def render_payload(message: CanonicalMessage) -> dict:
        """
        Convert CanonicalMessage into Bale API payload.
        """

        inline_keyboard = []
        for button in message.buttons + message.button_links:
            inline_keyboard.append([{
                "text": button.text,
                "url": button.target
            }])
        
        payload = {
            "text": message.text,
            "reply_markup": {"inline_keyboard": inline_keyboard}
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
