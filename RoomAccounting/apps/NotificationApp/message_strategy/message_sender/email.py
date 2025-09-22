from .interface import MessageSenderInterface


class EmailSender(MessageSenderInterface):
    
    def __init__(self, message_type, context):
        self.build_payload(message_type, context)
    
    def build_payload(self, message_type, context):
        text = f'Your _payload is {context}'
        self._payload = text
        print(f'payload setted: {text}')
    
    @property
    def payload(self):
        return self._payload
    
    def send(self):
        print(f'Sending ... {self.payload}')
