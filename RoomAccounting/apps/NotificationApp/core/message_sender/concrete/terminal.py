from ..interface.sender_interface import MessageSenderInterface
from apps.NotificationApp.core.message_types import BUILDER_MAP
from apps.NotificationApp.core.message_types.interface.builder_interface import MessageBuilderInterface


class TerminalSender(MessageSenderInterface):
    
    def __init__(self, message_type, context):
        self.build_payload(message_type, context)
    
    def build_payload(self, message_type, context):
        builder: MessageBuilderInterface = BUILDER_MAP[message_type]()
        text = builder.build_message(context)
        self._message = text
        self._to = context["identifier"]
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
