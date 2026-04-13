from .....dispatching.dispatcher import NotificationDispatcher

from .message import OtpMessage


@staticmethod
def send_otp(user, code: str):
    
    data = OtpMessage.Data(code=code)

    NotificationDispatcher.send(
        user,
        OtpMessage,
        data,
    )
