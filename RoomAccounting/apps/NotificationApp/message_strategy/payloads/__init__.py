from .concrete.otp import OtpPayload


PAYLOAD_MAP = {
    "otp": OtpPayload,
}


__all__ = ["PAYLOAD_MAP"]
