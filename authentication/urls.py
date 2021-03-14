from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from .views import *


app_name = 'auth'


urlpatterns = [
    path('validate-username/', csrf_exempt(UsernameValidaiton.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(EmailValidaiton.as_view()), name='validate-email'),
    
    path('register/', csrf_exempt(RegisterView.as_view()), name='register'),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
]
