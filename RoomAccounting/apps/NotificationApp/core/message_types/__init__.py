from .concrete import OtpDraft
from .concrete import ResetPasswordDraft

from .concrete.otp.builder import OTPBuilder
from .concrete.reset_password.builder import ResetPasswordBuilder


PAYLOAD_MAP = {
    "otp": OtpDraft,
    "reset_password": ResetPasswordDraft,
}


__all__ = ["PAYLOAD_MAP"]
