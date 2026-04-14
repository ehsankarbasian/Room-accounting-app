from .internal_routing.factory import make_feature_path

from .internal_features.verification.views import verification_view
from .internal_features.otp.views import send_otp_view, verify_otp_view


verification_path = make_feature_path(
    view=verification_view,
    default_route="verify/<str:token>/",
)

send_otp_path = make_feature_path(
    view=send_otp_view,
    default_route="send_otp",
)

verify_otp_path = make_feature_path(
    view=verify_otp_view,
    default_route="verify_otp/<str:code>/",
)
