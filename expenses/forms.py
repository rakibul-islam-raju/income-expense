from django import forms

from django.contrib.auth.models import User

from .models import *



class ExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['owner']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'amount': forms.TextInput(attrs={'placeholder': 'Amount'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            # 'category': forms.TextInput(attrs={'placeholder': 'Category'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': '2'}),
        }


# Expense formset
ExpenseCreateFormSet = forms.inlineformset_factory(
    User,
    Expense,
    ExpenseCreateForm,
    extra=3,
    can_delete=False
)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['owner']
