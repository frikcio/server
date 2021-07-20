from PIL import Image
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


class AvatarForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = get_user_model()
        fields = ('avatar', 'x', 'y', 'width', 'height',)

    def save(self):
        form = super(AvatarForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        image = Image.open(form.avatar)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(form.avatar.path)
        return form
