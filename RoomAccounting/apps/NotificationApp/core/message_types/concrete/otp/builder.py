from ...interface.builder_interface import MessageBuilderInterface


class OTPBuilder(MessageBuilderInterface):
    
    def build_message(self, context: dict):
        text = f"Your temp code is {context['code']}"
        return text
