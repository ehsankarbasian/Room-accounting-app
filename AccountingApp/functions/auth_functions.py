from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.template.loader import get_template

from rest_framework.decorators import api_view

from AccountingApp.models import *
from RoomAccounting.settings import HOST, PORT, ROOM_ACCOUNTING_APP_BASE_URL
from .helper_functions import send_email, result_page, send_room_log_email


@require_http_methods(["POST"])
def sign_up(request):
    fullname = request.POST['fullname']
    phone_number = request.POST['phone_number']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']

    verify_email_token = token_hex(64)
    token = Token.objects.create(verify_email_token=verify_email_token,
                                 verify_email_code=randint(100000, 999999))

    user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email,
                                    phone_number=phone_number,
                                    fullname=fullname,
                                    token=token)

    send_email_to_new_user(user)

    return result_page(request, "Signed up successfully,"
                                + " now verify at least one of your email or phone number and then sign in please")


def send_email_to_new_user(user):
    message = "Hello " + user.fullname + ". please click on the button below to verify your email"
    context = {'HOST': HOST,
               'PORT': PORT,
               'email': user.email,
               'name': user.username,
               'mode': 'verifyEmail',
               'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
               'verify_email_token': user.verify_email_token}
    html_content = get_template('email_verification.html').render(context=context)
    send_email("Verify email", message, [user.email], html_content)


@api_view(['POST'])
def verify_email(request):
    token = request.POST['token']
    email = request.POST['email']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return result_page(request, "User not found")

    user = user[0]
    if user.verified_email:
        return result_page(request, "Your email verified before")

    if token != user.token.verify_email_token:
        return result_page(request, "Wrong token")

    user.verified_email = True
    user.save()
    return result_page(request, "Email verified successfully. you can sign in.")


@api_view(['POST'])
def verify_person_email(request):
    token = request.POST['token']
    person_id = int(request.POST['person_id'])

    person = Person.objects.filter(id=person_id)
    if person.count() == 0:
        return result_page(request, "Person not found")

    person = person[0]
    if person.verified_email:
        return result_page(request, "Your email verified before")

    if token != person.verify_email_token:
        return result_page(request, "Wrong token")

    person.verify_email()
    send_room_log_email(person)
    return result_page(request, "Email verified successfully")


def forgot_password(request):
    email = request.GET['email']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return result_page(request, "User not found")

    user = user[0]
    reset_password_token = user.token.reset_pass_token
    send_reset_pass_email(email, user.fullname, reset_password_token)

    return result_page(request, "Email sent")


def send_reset_pass_email(email, fullname, token):
    context = {
        'HOST': HOST,
        'PORT': PORT,
        'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
        'email': email,
        'name': fullname,
        'token': token}
    html_content = get_template('reset_password.html').render(context=context)
    send_email(subject='reset password',
               message='message',
               to_list=[email],
               html_content=html_content)


@api_view(['POST'])
def reset_password_token_based(request):
    token = request.POST['token']
    email = request.POST['email']
    password_1 = request.POST['password_1']
    password_2 = request.POST['password_2']

    user = User.objects.filter(email=email)
    if user.count() == 0:
        return result_page(request, "User not found")

    if password_1 != password_2:
        return result_page(request, "the passwords are not equal")

    user = user[0]
    if not user.verified_email:
        return result_page(request, "Your email is not verified")

    if user.token.reset_pass_token != token:
        print(user.token.reset_pass_token)
        print(token)
        return result_page(request, "Wrong token")

    user.set_password(password_1)
    user.token.reset_pass_token = token_hex(64)
    user.save()
    return result_page(request, "Password changed successfully. you can sign in.")


@require_http_methods(["POST"])
def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is None:
        return result_page(request, "Wrong username/password")

    if not (user.verified_email or user.verified_phone):
        return result_page(request, "Verify at least one of your email or phone number to sign in")

    login(request, user)
    return redirect('home')


def log_out(request):
    logout(request)
    return redirect('landing_page')
