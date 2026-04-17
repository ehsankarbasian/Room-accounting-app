from django.http import HttpResponse, JsonResponse

from ......token_generator import TokenGenerator

from .service import send_otp as _send_otp
from .service import verify_otp as _verify_otp


def send_otp_view(request):
    
    code = TokenGenerator.generate()
    _send_otp(request.user, code)
    
    return HttpResponse("Code sent successfully")


def verify_otp_view(request, code):
    
    result = _verify_otp(request.user, code)
    return JsonResponse({"valid": result})
