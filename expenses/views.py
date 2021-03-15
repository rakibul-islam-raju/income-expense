from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    login_url = '/auth/login/'
    template_name = 'dashboard.html'
