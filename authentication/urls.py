from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


app_name = 'auth'


urlpatterns = [
    path('validate-username/', csrf_exempt(UsernameValidaiton.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(EmailValidaiton.as_view()), name='validate-email'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', csrf_exempt(RegisterView.as_view()), name='register'),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),

    path('request-reset-link/', RequestResetPassword.as_view(), name='request-reset-password'),
    path('set-password/<uidb64>/<token>/', CompletePasswordReset.as_view(), name='set-password'),
]
