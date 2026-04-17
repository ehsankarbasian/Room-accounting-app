from .internal.routing.factory import make_feature_path

from .internal.features.verification.views import verification_view
from .internal.features.otp.views import send_otp_view, verify_otp_view
from .internal.features.forgot_password.views import forgot_password_view, ResetPasswordByToken


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


send_forgot_password_message_path = make_feature_path(
    view=forgot_password_view,
    default_route="forgot_password",
)

reset_password_path = make_feature_path(
    view=ResetPasswordByToken,
    default_route="reset_password",
)
