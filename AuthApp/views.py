from secrets import token_hex

from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.template.loader import get_template

from ReportApp.models import User
from utils.email import send_email

from utils.custom_views.views import RawTemplateView
from django.views.generic.base import View

from AuthApp.persmissions.mixins import PermissionMixin
from AuthApp.persmissions.permissions import IsAuthenticated, IsAnonymous


class SignUpView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAnonymous, )
    template_name = "result.html"

    def post(self, request):
        fullname = request.POST['fullname']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username,
                                password=password,
                                email=email,
                                phone_number=phone_number,
                                fullname=fullname)
        
        context = {"result": "Signed up successfully"}
        return self.render_to_response(context)


class SignInView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAnonymous, )
    template_name = "result.html"
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            context = {'result': "Wrong username/password"}
            return self.render_to_response(context, status=status.HTTP_401_UNAUTHORIZED)

        # if not (user.verified_email or user.verified_phone):
        #     context = {'result': "Verify at least one of your email or phone number to sign in"}
            # return self.render_to_response(context, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return redirect('ReportApp:home')


class LogOutView(PermissionMixin, View):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        logout(request)
        return redirect('landing_page')


class ForgotPasswordView(PermissionMixin, RawTemplateView):
    permission_classes = (IsAnonymous, )
    template_name = "result.html"
    
    def get(self, request):
        email = request.GET['email']

        user = User.objects.filter(email=email)
        if user.count() == 0:
            context = {'result': "User not found"}
            return self.render_to_response(context, status=status.HTTP_404_NOT_FOUND)

        user = user[0]
        reset_password_token = user.token.reset_pass_token
        self._send_reset_pass_email(email, user.fullname, reset_password_token)

        context={'result': "Email sent"}
        return self.render_to_response(context)
    
    
    def _send_reset_pass_email(email, fullname, token):
        context = {
            # 'HOST': HOST,
            # 'PORT': PORT,
            # 'app_base_url': ROOM_ACCOUNTING_APP_BASE_URL,
            'email': email,
            'name': fullname,
            'token': token}
        html_content = get_template('AuthApp/reset_password.html').render(context=context)
        send_email(subject='reset password',
                message='message',
                to_list=[email],
                html_content=html_content)


class ResetPasswordByTokenAPI(PermissionMixin, APIView):
    permission_classes = (IsAnonymous, )
    
    def post(self, request):
        token = request.POST['token']
        email = request.POST['email']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        user = User.objects.filter(email=email)
        if user.count() == 0:
            return self._render_result("User not found")

        if password_1 != password_2:
            return self._render_result("the passwords are not equal")

        user = user[0]
        if not user.verified_email:
            return self._render_result("Your email is not verified")

        if user.token.reset_pass_token != token:
            print(user.token.reset_pass_token)
            print(token)
            return self._render_result("Wrong token")

        user.set_password(password_1)
        user.token.reset_pass_token = token_hex(64)
        user.save()
        return self._render_result("Password changed successfully. you can sign in.")

    
    def _render_result(self, result):
        return render(self.request, 'result.html', context={'result': result})
