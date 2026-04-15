from django.http import HttpResponse

from django.contrib.auth import get_user_model
User = get_user_model()

from .service import send_forgot_password


def forgot_password_view(request):
    
    email = request.GET['email']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return HttpResponse("User not found")

    user = user[0]
    send_forgot_password(user, code='*__TODO__*')

    return HttpResponse("Message sent")
