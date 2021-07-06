from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from accounts.models import RemindAccess


class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class RemindForm(ModelForm):
    class Meta:
        model = RemindAccess
        fields = ['remind']
