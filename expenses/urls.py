from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


app_name = 'expenses'


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('expense-create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('expense/<int:pk>/edit/', ExpenseEditView.as_view(), name='expense_edit'),
    path('expense/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
    path('expenses/search-expenses', csrf_exempt(SerchExpenses.as_view()), name='expense_search'),
    path('expenses/summary-data', csrf_exempt(ExpenseSummaryData.as_view()), name='expense_summary_data'),
    path('expenses/summary/', ExpenseSummaryView.as_view(), name='expense_summary'),
    path('expenses/export_csv/', export_csv, name='export_csv'),
]