from core.sms_client import send_text_sms

from apps.NotificationApp.interfaces import MessageSenderInterface

from ..message_schema import CanonicalMessage


class SmsSender(MessageSenderInterface):
    """
    This is currently a placeholder and should be implemented
    using an SMS provider.
    """
    
    sender_key = "sms"
    
    @staticmethod
    def render_payload(message: CanonicalMessage):
        
        buttons_as_text = ""
        for button in message.buttons + message.button_links:
            buttons_as_text += f'\n{button.text}:\n{button.target}\n'
        
        final_text = message.text + "\n" + buttons_as_text
        return {"text": final_text}
        
    
    @staticmethod
    def send_payload(identifier: str, payload: dict):
        
        print("\n", "-" * 100)
        print("\nSending ...\n")

        print("SMS text: ", payload['text'])

        print("\nmessage receiver identifier:")
        print(f"    {identifier}")

        print("\n", "-" * 100, "\n")
        
        
        # send_text_sms(message=payload['text'], to=identifier)
