from django import forms
from django.contrib.auth.models import User


# class Loginform(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['']


class Registerform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
