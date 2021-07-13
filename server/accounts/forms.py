from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import Settings


# Get qoups queryset
groups_list = Group.objects.all()

# Creating CHOICES, depend on groups count
GROUP_CHOICES = ([(group.pk, group) for group in groups_list])


class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    groups = forms.ChoiceField(choices=GROUP_CHOICES, required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'groups']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['periodic_mailing']
