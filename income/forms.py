from django import forms

from django.contrib.auth.models import User

from .models import *



class IncomeCreateForm(forms.ModelForm):
    class Meta:
        model = Income
        exclude = ['owner']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'amount': forms.TextInput(attrs={'placeholder': 'Amount'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': '2'}),
        }


# Expense formset
IncomeCreateFormSet = forms.inlineformset_factory(
    User,
    Income,
    IncomeCreateForm,
    extra=3,
    can_delete=False
)


class SourceCreateForm(forms.ModelForm):
    class Meta:
        model = Source
        exclude = ['owner']
