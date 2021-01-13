from django.shortcuts import render
from django.views import View
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.validators import UnicodeUsernameValidator

# from validate_email import validate_email

from .forms import *

import json


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
        # return JsonResponse({'email_valid': True})


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

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
    
            messages.success(request, 'Registration Successfull.')
        else:
            messages.error(request, 'Invalid form.')

        context = {
            'form': form
        }

        return render(request, 'auth/register.html', context)
