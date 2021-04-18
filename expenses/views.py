import json
import datetime

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


class ExpenseSummaryData(View):
    def get(self, request, *args, **kwargs):
        todays_date = datetime.date.today()
        last_month = todays_date - datetime.timedelta(days=30)

        expenses = Expense.objects.filter(date__gte=last_month, date__lte=todays_date)

        finalrep = {}

        def get_category(expense):
            return expense.category
        category_list = list(set(map(get_category, expenses)))

        def get_expense_category_amount(category):
            amount = 0
            filtered_by_category = expenses.filter(category=category)

            for item in filtered_by_category:
                amount += item.amount
            return amount

        for x in expenses:
            for y in category_list:
                finalrep[y.name] = int(get_expense_category_amount(y))

        return JsonResponse({'expense_category_data': finalrep}, safe=False)


class ExpenseSummaryView(View):
    def get(self, request):
        return render(request, 'expenses/expense_summary.html')
