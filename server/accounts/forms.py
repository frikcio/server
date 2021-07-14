from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .choices import GroupChoices
from .models import Settings


class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    groups = forms.ChoiceField(choices=GroupChoices.choices, required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'groups']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['periodic_mailing']
