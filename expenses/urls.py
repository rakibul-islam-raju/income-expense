from django.urls import path

from .views import *


app_name = 'expenses'


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]