from .concrete import OtpPayload
from .concrete import ResetPasswordPayload

from .concrete.otp.builder import OTPBuilder
from .concrete.reset_password.builder import ResetPasswordBuilder


PAYLOAD_MAP = {
    "otp": OtpPayload,
    "reset_password": ResetPasswordPayload,
}

BUILDER_MAP = {
    "otp": OTPBuilder,
    "reset_password": ResetPasswordBuilder,
}


__all__ = ["PAYLOAD_MAP", "BUILDER_MAP"]
