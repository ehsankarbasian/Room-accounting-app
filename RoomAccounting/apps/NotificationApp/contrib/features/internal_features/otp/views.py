from django.http import HttpResponse

from .....token_generator import TokenGenerator
from .service import send_otp as _send_otp


def otp_view(request):
    
    code = TokenGenerator.generate()
    _send_otp(request.user, code)
    
    return HttpResponse("Code sent successfully")
