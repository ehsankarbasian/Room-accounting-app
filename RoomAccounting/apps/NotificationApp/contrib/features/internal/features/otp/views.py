from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.urls import reverse

from ......token_generator import TokenGenerator

from ...utils.url_namespace import get_complete_view_url_name

from .service import send_otp as _send_otp
from .service import verify_otp as _verify_otp


def send_otp_view(request):
    
    code = TokenGenerator.generate()
    url_name = get_complete_view_url_name(view=verify_otp_view)
    verify_otp_path = reverse(url_name, kwargs={'code': code})
    verify_otp_url = f"{settings.SITE_BASE_URL}{verify_otp_path}"
    
    _send_otp(request.user, code, verify_otp_url)
    
    return HttpResponse("Code sent successfully")


def verify_otp_view(request, code):
    
    result = _verify_otp(request.user, code)
    return JsonResponse({"valid": result})
