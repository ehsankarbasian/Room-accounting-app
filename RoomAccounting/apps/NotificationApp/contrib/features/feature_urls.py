from .internal_routing.factory import make_feature_path

from .internal_features.verification.views import verification_view
from .internal_features.otp.views import otp_view


verification_path = make_feature_path(
    view=verification_view,
    default_route="verify/<str:token>/",
)

otp_path = make_feature_path(
    view=otp_view,
    default_route="send_otp",
)
