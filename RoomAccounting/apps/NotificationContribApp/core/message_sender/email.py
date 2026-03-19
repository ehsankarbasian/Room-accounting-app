from django.core.mail import send_mail as _send_mail
from django.core.mail import EmailMultiAlternatives as _Email

from core.settings import DEFAULT_FROM_EMAIL

from apps.NotificationApp.core.registry import SenderRegistry, BuilderRegistry
from apps.NotificationApp.core.interfaces.sender_interface import MessageSenderInterface
from apps.NotificationApp.core.interfaces.builder_interface import MessageBuilderInterface

def _send_html_email(subject, message, to_list, html_content):
    email_obj = _Email(
        subject=subject,
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=to_list)
    email_obj.attach_alternative(html_content, "text/html")
    email_obj.send()


def _send_text_email(subject, message, to_list):
    _send_mail(
        subject=subject,
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=to_list)


@SenderRegistry.register(name="email")
class EmailSender(MessageSenderInterface):
    
    def __init__(self, message_type, context):
        self.build_payload(message_type, context)
    
    def build_payload(self, message_type, context):
        builder: MessageBuilderInterface = BuilderRegistry.REGISTRY[message_type]()
        text = builder.build_message(context)
        self._message = text
        self._to = context["identifier"]
        print(f'builde message setted: {text}')
    
    @property
    def message(self):
        return self._message
    
    def send(self):
        print(f'Sending ... {self.message}')
        html_content = self.message
        _send_html_email(subject='reset password',
                message='message',
                to_list=[self._to],
                html_content=html_content)
