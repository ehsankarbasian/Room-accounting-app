from ..message_types.concrete.otp.otp import OtpPayload
from ..message_types.concrete.reset_password.reset_password import ResetPasswordPayload


PAYLOAD_MAP = {
    "otp": OtpPayload,
    "reset_password": ResetPasswordPayload,
}


__all__ = ["PAYLOAD_MAP"]
