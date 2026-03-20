import json
import requests

from core.settings import BALE_BOT_TOKEN

from apps.NotificationApp.core.registry import SenderRegistry, BuilderRegistry
from apps.NotificationApp.core.interfaces import MessageSenderInterface, MessageBuilderInterface

from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(name=SenderType.BALE)
class BaleSender(MessageSenderInterface):
    
    def __init__(self, message_type, data, identifier):
        self._to = identifier
        self.build_payload(message_type, data)
    
    def build_payload(self, message_type, data):
        builder: MessageBuilderInterface = BuilderRegistry.REGISTRY[message_type]()
        text = builder.build_message(data)
        self._message = text
        print(f'builde message setted: {text}')
    
    @property
    def message(self):
        return self._message
    
    def send(self):
        url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendMessage"
        
        data = {
            "chat_id": 1435368642,
            "text": self.message,
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "ورود یکبار مصرف",
                            "url": "https://zarebin.ir"
                        }
                    ]
                ]
            }
        }
        
        response = requests.post(url=url, json=data)
