import json

from django.shortcuts import redirect, render
from django.views import View
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from .forms import *
from .utils import token_generator, EmailThread

class UsernameValidaiton(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data['username']

        # check for alphanemeric charecters
        if not str(username).isalnum():
            return JsonResponse({
                'username_error': 'Username should only contains alphanemeric charecters.'
            }, status=400)

        # check for existing username
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error': 'This username is already taken.'
            }, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidaiton(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data['email']

        # check for existing email
        if not User.objects.filter(email=email).exists():
            # check for valid email
            try:
                validate_email(email)
                return JsonResponse({
                    'email_valid': True
                }, status=200)
            except:
                return JsonResponse({
                    'email_error': 'Invalid Email.'
                }, status=400)
        else:
            return JsonResponse({
                'email_error': 'This email is already used.'
            }, status=409)


class RegisterView(View):
    def get(self, request):
        form = Registerform()
        context = {
            'form': form
        }
        return render(request, 'auth/register.html', context)

    def post(self, request):
        form = Registerform(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Create New User
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            messages.success(request, 'Registration Successfull.')

            # Generate activacation url
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('auth:activate', kwargs={
                           'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = 'http://'+domain+link

            # Send email
            email_subject = 'Activate Your Account'
            email_body = 'Hello ' + user.username + \
                ', Please use this link to verify your account.\n' + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'no-reply@domain.com',  # from
                [email, ]  # recipient
            )
            EmailThread(email).start()
            messages.success(
                request, 'Account activation email has been sent to your email.')
        else:
            messages.error(request, 'Invalid form.')

        context = {
            'form': form
        }

        return render(request, 'auth/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            # decode user_id
            _id = force_text(urlsafe_base64_decode(uidb64))
            # get exact user
            user = User.objects.get(pk=_id)

            # check if token already verified
            if not token_generator.check_token(user, token):
                messages.info(request, 'User already activated.')
                return redirect('auth:login')
            # check if user already acticated
            elif user.is_active:
                messages.info(request, 'User already activated.')
                return redirect('auth:login')
            # if user not activated or not token is verified
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Account acctivated successfully..')
                return redirect('auth:login')
        except Exception as ex:
            pass

        return redirect('auth:login')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            # if user exists
            if user:
                # if user is verified
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request, f'Welcome, {user.username}. You are now logged in.')
                    return redirect('expenses:dashboard')
                else:
                    # if user is not verified
                    messages.error(request, 'Account not verified.')
                    # TODO: sent verification email
                    return redirect('auth:login')
            else:
                # if user does not exist
                messages.error(request, 'Invalid Credentials.')
                return redirect('auth:login')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('auth:login')


class RequestResetPassword(View):
    def get(self, request):
        return render(request, 'auth/reset-password.html')

    def post(self, request):
        email = request.POST.get('email')

        user = User.objects.filter(email=email).first()
        if user is not None:
            # Generate activacation url
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('auth:set-password', kwargs={
                'uidb64': uidb64, 'token': PasswordResetTokenGenerator().make_token(user)})
            activate_url = 'http://'+domain+link

            # Send email
            email_subject = 'Reset Password'
            email_body = 'Hello ' + user.username + \
                ', Please use this link to reset your password.\n' + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'no-reply@domain.com',  # from
                [email, ]  # recipient
            )
            EmailThread(email).start()
            messages.success(
                request, 'Password reset email has been sent to your email.')
            return redirect('./')
        else:
            messages.warning(
                request, 'No user is associated with this email.')
            return redirect('./')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                # import pdb ; pdb.set_trace()
                messages.info(
                    request, 'Password reset reset link is invalid. Please request for new one.')
                return render(request, 'auth/set-password.html', context)

        except Exception as identifier:
            messages.info(request, 'Something went wrong, please try again.')
            return render(request, 'auth/set-password.html', context)

        return render(request, 'auth/set-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Password did not match.')
            return redirect('./')

        if len(password) < 6:
            messages.error(request, 'Password too short.')
            return redirect('./')

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(
                request, 'Password reset successfully. Now you can login with your new password')
            return redirect('auth:login')
        except Exception as identifier:
            messages.info(request, 'Something went wrong, please try again.')
            return redirect('./')
