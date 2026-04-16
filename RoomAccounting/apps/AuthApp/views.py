from rest_framework import status

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from utils.custom_views.views import RawTemplateView
from django.views.generic.base import View

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.AuthApp.persmissions.mixins import PermissionMixin
from apps.AuthApp.persmissions.permissions import IsAuthenticated, IsAnonymous


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
