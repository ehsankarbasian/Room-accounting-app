from ..interface.sender_interface import MessageSenderInterface
from apps.NotificationApp.core.payloads import PAYLOAD_MAP


class EmailSender(MessageSenderInterface):
    
    def __init__(self, message_type, context):
        self.build_payload(message_type, context)
    
    def build_payload(self, message_type, context):
        payload = PAYLOAD_MAP[message_type]
        text = payload.build(context)
        self._payload = text
        print(f'payload setted: {text}')
    
    @property
    def payload(self):
        return self._payload
    
    def send(self):
        print(f'Sending ... {self.payload}')
