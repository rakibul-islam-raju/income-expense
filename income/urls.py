from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


app_name = 'income'


urlpatterns = [
    path('income-create/', IncomeCreateView.as_view(), name='income_create'),
    path('income/', IncomeListView.as_view(), name='income_list'),
    path('income/<int:pk>/edit/', IncomeEditView.as_view(), name='income_edit'),
    path('income/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income_delete'),
    path('income/search-income', csrf_exempt(SearchIncome.as_view()), name='income_search'),
]