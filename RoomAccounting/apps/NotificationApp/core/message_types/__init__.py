from .concrete import OtpPayload
from .concrete import ResetPasswordPayload


PAYLOAD_MAP = {
    "otp": OtpPayload,
    "reset_password": ResetPasswordPayload,
}


__all__ = ["PAYLOAD_MAP"]
