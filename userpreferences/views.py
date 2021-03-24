import os
import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *


class IndexView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get_preferences(self, request):
        ''' Check if user already has any preferences '''

        preferences = None
        exists = UserPreferences.objects.get(user=request.user)
        if exists:
            preferences = exists

        return preferences

    def get(self, request):
        # print(self.get_preferences(request).currency)

        currency_data = []
        # json file path
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        # append currency data to python list
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})

        context = {
            'currencies': currency_data,
            'preferences': self.get_preferences(request)
        }
        return render(request, 'preferences/index.html', context)

    def post(self, request):
        currency = request.POST['currency']
        preferrences = self.get_preferences(request)
        if preferrences:
            preferrences.currency = currency
            preferrences.save()
        else:
            UserPreferences.objects.create(
                user=request.user, currency=currency)

        messages.success(request, 'Changes Saved')
        return redirect('preferences:index')
