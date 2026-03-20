from apps.NotificationApp.core.registry import SenderRegistry, BuilderRegistry
from apps.NotificationApp.core.interfaces import MessageSenderInterface, MessageBuilderInterface

from apps.NotificationContribApp.notification_types import SenderType


@SenderRegistry.register(name=SenderType.TERMINAL)
class TerminalSender(MessageSenderInterface):
    
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
        print('\n', '-'*80)
        
        print('\nSending ...')
        
        print('\nmessage:')
        print(f'    {self.message}')
        
        print('\nmessage reciever identifier:')
        print(f'    {self._to}')
        
        print('\n', '-'*80, '\n')
