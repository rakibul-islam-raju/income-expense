from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import JsonResponse

from .forms import *
from .models import *

import json


class SearchIncome(View):
    def post(self, request, *args, **kwargs):
        search_str = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(
            title__icontains=search_str, owner=self.request.user
        ) | Income.objects.filter(
            amount__icontains=search_str, owner=self.request.user
        ) | Income.objects.filter(
            description__icontains=search_str, owner=self.request.user
        ) | Income.objects.filter(
            date__icontains=search_str, owner=self.request.user
        ) | Income.objects.filter(
            source__name__icontains=search_str, owner=self.request.user
        )

        sources = Source.objects.filter(
            owner=self.request.user
        )

        data = {
            'incomes': list(incomes.values()),
            'sources': list(sources.values())
        }

        return JsonResponse(data, safe=False)


class IncomeListView(LoginRequiredMixin, ListView):
    template_name = 'income/index.html'
    context_object_name = 'incomes'
    paginate_by = 20

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)


class IncomeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'income/add_income.html'

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)

    def get_form(self, form_class=None):
        return IncomeCreateFormSet(**self.get_form_kwargs())

    def form_valid(self, form):
        owner = self.request.user
        instances = form.save(commit=False)
        for instance in instances:
            instance.owner = owner
            instance.save()
            messages.success(self.request, 'Income added successfully.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse('income:income_list')


class IncomeEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'income/edit_income.html'
    form_class = IncomeCreateForm
    success_message = 'Income Updated'
    success_url = reverse_lazy('income:income_list')

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    success_url = reverse_lazy('income:income_list')

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)
