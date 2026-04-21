from .internal.features.otp.service import send_otp, verify_otp
from .internal.features.forgot_password.service import send_forgot_password

from .internal.features.forgot_password.message import ForgotPasswordMessage as _ForgotPasswordMessage
from .internal.features.verification.message import VerifyChannelMessage as _VerifyChannelMessage
from .internal.features.otp.message import OtpMessage as _OtpMessage


class MessageClasses:
    ForgotPasswordMessage = _ForgotPasswordMessage
    VerifyChannelMessage = _VerifyChannelMessage
    OtpMessage = _OtpMessage
