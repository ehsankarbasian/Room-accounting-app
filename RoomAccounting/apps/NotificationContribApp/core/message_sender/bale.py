from typing import Any

import requests

from core.settings import BALE_BOT_TOKEN

from apps.NotificationApp.core.registry import SenderRegistry
from apps.NotificationApp.core.interfaces import MessageSenderInterface

from apps.NotificationContribApp.core.models.canonical import NotificationCanonicalMessage, Button
from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(name=SenderType.BALE)
class BaleSender(MessageSenderInterface):

    def __init__(self, identifier: Any):
        self._identifier = identifier  # chat_id


    def render_payload(self, message: NotificationCanonicalMessage) -> dict:
        """
        Converts the canonical NotificationMessage to a Bale-specific payload.
        """

        payload = {
            "chat_id": self._identifier,
            "text": message.text
        }

        # اگر دکمه وجود دارد، تبدیل به inline_keyboard مخصوص بله
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


    def send(self, payload: dict):
        """
        Sends the payload to Bale API.
        """
        url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendMessage"
        response = requests.post(url=url, json=payload)
        response.raise_for_status()

        return response
