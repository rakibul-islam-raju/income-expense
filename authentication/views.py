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


from .forms import *
from .utils import token_generator


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
                [email,]  # recipient
            )
            email.send(fail_silently=False)
            messages.success(request, 'Account activation email has been sent to your email.')
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
