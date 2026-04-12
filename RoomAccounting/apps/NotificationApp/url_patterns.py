from .factory import make_feature_path
from .contrib.features.verification.views import verification_view


app_name = "NotificationApp"


verification_path = make_feature_path(
    view=verification_view,
    default_route="verify/<str:token>/",
)
