import hashlib

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from django.contrib.auth import get_user_model
User = get_user_model()

from .....token_generator.default import NumericSixDigitTokenGenerator

from .service import send_forgot_password
from .query import get_latest_valid_reset_password_token


def forgot_password_view(request):
    
    email = request.GET['email']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return HttpResponse("User not found")

    user = user[0]
    
    code = NumericSixDigitTokenGenerator.generate()
    send_forgot_password(user, code=code)

    return HttpResponse("Message sent")


class ResetPasswordByToken(View):
    
    def get(self, request):
        return render(request, "forgot_password/reset_password.html")
        
    
    def post(self, request):
        token = request.POST['token']
        email = request.POST['email']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        user = User.objects.filter(email=email)
        if user.count() == 0:
            return HttpResponse("User not found")

        if password_1 != password_2:
            return HttpResponse("the passwords are not equal")

        user = user[0]
        if not user.verified_email:
            return HttpResponse("Your email is not verified")
        
        selector = f"user:{user.id}:reset_password"
        saved_token = get_latest_valid_reset_password_token(selector)
        
        if not saved_token:
            return HttpResponse("Code not found. Please try again")

        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        
        if saved_token.token_hash != token_hash:
            return HttpResponse("Wrong code")

        user.set_password(password_1)
        user.save()
        
        saved_token.is_used = True
        saved_token.save(update_fields=["is_used"])
        
        return HttpResponse("Password changed successfully. you can sign in.")
