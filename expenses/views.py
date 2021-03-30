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


class SerchExpenses(View):
    def post(self, request, *args, **kwargs):
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            title__icontains=search_str, owner=self.request.user
        ) | Expense.objects.filter(
            amount__icontains=search_str, owner=self.request.user
        ) | Expense.objects.filter(
            description__icontains=search_str, owner=self.request.user
        ) | Expense.objects.filter(
            date__icontains=search_str, owner=self.request.user
        ) | Expense.objects.filter(
            category__name__icontains=search_str, owner=self.request.user
        )

        categories = Category.objects.filter(
            owner=self.request.user
        )

        data = {
            'expenses': list(expenses.values()),
            'categories': list(categories.values())
        }

        # print(list(data))


        return JsonResponse(data, safe=False)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class ExpenseListView(LoginRequiredMixin, ListView):
    template_name = 'expenses/index.html'
    context_object_name = 'expenses'
    paginate_by = 20

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'expenses/add_expenses.html'

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)

    def get_form(self, form_class=None):
        return ExpenseCreateFormSet(**self.get_form_kwargs())

    def form_valid(self, form):
        owner = self.request.user
        instances = form.save(commit=False)
        for instance in instances:
            instance.owner = owner
            instance.save()
            messages.success(self.request, 'Expenses added successfully.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse('expenses:expense_list')


class ExpenseEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'expenses/edit_expenses.html'
    form_class = ExpenseCreateForm
    success_message = 'Expense Updated'
    success_url = reverse_lazy('expenses:expense_list')

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    success_url = reverse_lazy('expenses:expense_list')

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)
